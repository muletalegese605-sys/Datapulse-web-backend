/* DataPulse Cloud Functions v7 */
const { onCall, onRequest, HttpsError } = require("firebase-functions/v2/https");
const { onSchedule } = require("firebase-functions/v2/scheduler");
const { onDocumentCreated } = require("firebase-functions/v2/firestore");
const { setGlobalOptions } = require("firebase-functions/v2");
const logger = require("firebase-functions/logger");
const admin = require("firebase-admin");
const axios = require("axios");
const crypto = require("crypto");

admin.initializeApp();
const db = admin.firestore();

setGlobalOptions({
  region: "europe-west1",
  maxInstances: 10,
  memory: "256MiB",
  timeoutSeconds: 60
});

async function isAdmin(uid) {
  if (!uid) return false;
  try {
    const snap = await db.collection("admins").doc(uid).get();
    if (!snap.exists) return false;
    return ["super","admin","support"].includes(snap.data().role);
  } catch (e) { return false; }
}

async function logAudit(action, target, payload, uid) {
  try {
    await db.collection("audits").add({
      action, target, payload: payload || {},
      org: (uid === "system") ? "[SYSTEM]" : "[USER]",
      admin: uid || "system", status: "SUCCESS",
      at: admin.firestore.FieldValue.serverTimestamp(),
      item_id: target
    });
  } catch (e) { logger.warn("Audit failed:", e.message); }
}

exports.health = onRequest({ cors: true }, async (req, res) => {
  res.json({ status: "ok", service: "DataPulse Functions", version: "7.0.0" });
});

let genAI = null;
function getGenAI() {
  if (!genAI) {
    const key = process.env.GEMINI_API_KEY;
    if (!key) throw new Error("GEMINI_API_KEY not set");
    const { GoogleGenerativeAI } = require("@google/generative-ai");
    genAI = new GoogleGenerativeAI(key);
  }
  return genAI;
}

exports.chatWithAI = onCall({ cors: true }, async (request) => {
  if (!request.auth) throw new HttpsError("unauthenticated", "Login required");
  const uid = request.auth.uid;
  const { message, lang = "en", context = {} } = request.data || {};
  if (!message) throw new HttpsError("invalid-argument", "message required");

  const today = new Date().toISOString().slice(0,10);
  const usageRef = db.collection("ai_usage").doc(uid + "_" + today);
  const usageSnap = await usageRef.get();
  const used = usageSnap.exists ? (usageSnap.data().count || 0) : 0;
  if (used >= 500) throw new HttpsError("resource-exhausted", "Daily AI limit reached");

  let orgData = {};
  try {
    const oSnap = await db.collection("orgs").doc(uid).get();
    if (oSnap.exists) orgData = oSnap.data();
  } catch (e) {}

  const langMap = { om:"Afaan Oromoo", am:"Amharic", ar:"Arabic", fr:"French", es:"Spanish", tr:"Turkish", ru:"Russian", sw:"Kiswahili", el:"Greek", hi:"Hindi", zh:"Chinese", en:"English" };
  const sysPrompt = "You are DataPulse AI. Answer in " + (langMap[lang] || "English") +
    ". Org: " + (orgData.name || "Unknown") +
    ". Records: " + (context.records || 0) +
    ". Sales: ETB " + (context.sales || 0) +
    ". Margin: " + (context.margin || 0) + "%. Be concise.";

  try {
    const model = getGenAI().getGenerativeModel({ model: "gemini-1.5-flash", systemInstruction: sysPrompt });
    const result = await model.generateContent(message);
    const reply = result.response.text();
    await usageRef.set({ count: admin.firestore.FieldValue.increment(1), uid }, { merge: true });
    await logAudit("AI_CHAT", uid, { lang });
    return { reply, usage: { used: used + 1, limit: 500 } };
  } catch (e) {
    logger.error("Gemini error:", e.message);
    throw new HttpsError("internal", "AI unavailable: " + e.message);
  }
});

exports.onDataRequestCreate = onDocumentCreated("data_requests/{requestId}", async (event) => {
  const snap = event.data;
  if (!snap) return;
  const req = snap.data();
  await logAudit("DATA_REQUEST_CREATED", snap.id, { org: req.orgName, type: req.type });
});

exports.onPaymentCreate = onDocumentCreated("payments/{paymentId}", async (event) => {
  const snap = event.data;
  if (!snap) return;
  const pay = snap.data();
  await logAudit("PAYMENT_CREATED", snap.id, { usd: pay.usd, method: pay.method });
});

exports.onContractCreate = onDocumentCreated("contracts/{contractId}", async (event) => {
  const snap = event.data;
  if (!snap) return;
  const c = snap.data();
  if (c.status !== "active") return;
  try {
    const orgRef = db.collection("orgs").doc(c.orgId);
    const oSnap = await orgRef.get();
    if (oSnap.exists) {
      const trial = oSnap.data().trial || {};
      trial.paid = true;
      trial.paidAt = new Date().toISOString();
      await orgRef.update({ plan: c.plan, trial });
    }
    await logAudit("CONTRACT_ACTIVATED", c.orgId, { plan: c.plan });
  } catch (e) { logger.error("onContractCreate failed:", e.message); }
});

exports.verifyPaystack = onCall({ cors: true }, async (request) => {
  if (!request.auth) throw new HttpsError("unauthenticated", "Login required");
  const { reference, planId, orgId } = request.data || {};
  if (!reference || !planId) throw new HttpsError("invalid-argument", "reference & planId required");
  const secretKey = process.env.PAYSTACK_SECRET_KEY;
  if (!secretKey) throw new HttpsError("failed-precondition", "Paystack not configured");
  try {
    const res = await axios.get("https://api.paystack.co/transaction/verify/" + reference, { headers: { Authorization: "Bearer " + secretKey } });
    if (!res.data.status || res.data.data.status !== "success") throw new Error("Payment not successful");
    const amount = res.data.data.amount / 100;
    const contractRef = db.collection("contracts").doc();
    await contractRef.set({
      id: contractRef.id, orgId: orgId || request.auth.uid,
      plan: planId, usd: amount, currency: "USD",
      method: "paystack", reference, status: "active",
      startedAt: admin.firestore.FieldValue.serverTimestamp(),
      expiresAt: new Date(Date.now() + 30 * 86400000)
    });
    await logAudit("PAYSTACK_VERIFY_SUCCESS", reference, { amount, planId });
    return { success: true, amount };
  } catch (e) {
    logger.error("Paystack verify failed:", e.message);
    throw new HttpsError("internal", "Verification failed: " + e.message);
  }
});

exports.paystackWebhook = onRequest({ cors: false }, async (req, res) => {
  if (req.method !== "POST") return res.status(405).send("Method not allowed");
  const secret = process.env.PAYSTACK_SECRET_KEY || "";
  const hash = crypto.createHmac("sha512", secret).update(JSON.stringify(req.body)).digest("hex");
  if (hash !== req.headers["x-paystack-signature"]) return res.status(401).send("Invalid signature");
  if (req.body.event === "charge.success") {
    await logAudit("PAYSTACK_WEBHOOK", req.body.data.reference, { amount: req.body.data.amount / 100 });
  }
  res.status(200).send("OK");
});

exports.dailyTrialCheck = onSchedule({ schedule: "0 9 * * *", timeZone: "Africa/Addis_Ababa" }, async (event) => {
  const now = Date.now();
  const tomorrow = now + 24 * 3600 * 1000;
  const orgsSnap = await db.collection("orgs").get();
  let expiringSoon = 0, expired = 0;
  for (const doc of orgsSnap.docs) {
    const org = doc.data();
    const trial = org.trial || {};
    if (trial.paid) continue;
    const endsAt = trial.endsAt ? new Date(trial.endsAt).getTime() : 0;
    if (!endsAt) continue;
    if (endsAt > now && endsAt <= tomorrow) expiringSoon++;
    else if (endsAt <= now) expired++;
  }
  await logAudit("DAILY_TRIAL_CHECK", "system", { expiringSoon, expired });
});

exports.getAdminMetrics = onCall({ cors: true }, async (request) => {
  if (!request.auth) throw new HttpsError("unauthenticated", "Login required");
  if (!await isAdmin(request.auth.uid)) throw new HttpsError("permission-denied", "Admin only");
  const orgsSnap = await db.collection("orgs").count().get();
  const contractsSnap = await db.collection("contracts").where("status", "==", "active").get();
  let mrr = 0;
  contractsSnap.docs.forEach((d) => { mrr += Number(d.data().usd || 0); });
  return { totalOrgs: orgsSnap.data().count, activeContracts: contractsSnap.size, mrrUsd: mrr };
});

exports.adminSuspendOrg = onCall({ cors: true }, async (request) => {
  if (!request.auth) throw new HttpsError("unauthenticated", "Login required");
  if (!await isAdmin(request.auth.uid)) throw new HttpsError("permission-denied", "Admin only");
  const { orgId, reason = "" } = request.data || {};
  if (!orgId) throw new HttpsError("invalid-argument", "orgId required");
  await db.collection("orgs").doc(orgId).update({
    status: "suspended",
    suspendedAt: admin.firestore.FieldValue.serverTimestamp(),
    suspendedBy: request.auth.uid, suspendReason: reason
  });
  await logAudit("ADMIN_SUSPEND_ORG", orgId, { reason });
  return { success: true };
});

exports.adminExtendTrial = onCall({ cors: true }, async (request) => {
  if (!request.auth) throw new HttpsError("unauthenticated", "Login required");
  if (!await isAdmin(request.auth.uid)) throw new HttpsError("permission-denied", "Admin only");
  const { orgId, days = 14 } = request.data || {};
  if (!orgId) throw new HttpsError("invalid-argument", "orgId required");
  const orgRef = db.collection("orgs").doc(orgId);
  const snap = await orgRef.get();
  if (!snap.exists) throw new HttpsError("not-found", "Org not found");
  const trial = snap.data().trial || {};
  trial.endsAt = new Date(Date.now() + days * 86400000).toISOString();
  trial.paid = false;
  await orgRef.update({ trial });
  await logAudit("ADMIN_EXTEND_TRIAL", orgId, { days });
  return { success: true, newEndsAt: trial.endsAt };
});

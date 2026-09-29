const express = require("express");
const cors = require("cors");
require("dotenv").config();

const app = express();
app.use(cors({ origin: "*" }));
app.use(express.json());

const PROJECT_ID = process.env.FIREBASE_PROJECT_ID;
const API_KEY = process.env.FIREBASE_API_KEY;
const BASE_URL = `https://firestore.googleapis.com/v1/projects/${PROJECT_ID}/databases/(default)/documents`;

// ===== Firestore REST helpers =====
function toFs(val) {
  if (val === null || val === undefined) return { nullValue: null };
  if (typeof val === "string") return { stringValue: val };
  if (typeof val === "boolean") return { booleanValue: val };
  if (typeof val === "number") {
    return Number.isInteger(val) ? { integerValue: String(val) } : { doubleValue: val };
  }
  if (Array.isArray(val)) return { arrayValue: { values: val.map(toFs) } };
  if (typeof val === "object") {
    const fields = {};
    for (const k in val) fields[k] = toFs(val[k]);
    return { mapValue: { fields } };
  }
  return { stringValue: String(val) };
}

function fromFs(v) {
  if (!v) return null;
  if ("stringValue" in v) return v.stringValue;
  if ("integerValue" in v) return Number(v.integerValue);
  if ("doubleValue" in v) return v.doubleValue;
  if ("booleanValue" in v) return v.booleanValue;
  if ("nullValue" in v) return null;
  if ("timestampValue" in v) return v.timestampValue;
  if ("arrayValue" in v) return (v.arrayValue.values || []).map(fromFs);
  if ("mapValue" in v) {
    const out = {};
    const fields = v.mapValue.fields || {};
    for (const k in fields) out[k] = fromFs(fields[k]);
    return out;
  }
  return null;
}

function docToObj(doc) {
  const out = { _id: doc.name ? doc.name.split("/").pop() : null };
  const fields = doc.fields || {};
  for (const k in fields) out[k] = fromFs(fields[k]);
  return out;
}

async function listDocs(collection) {
  const r = await fetch(`${BASE_URL}/${collection}?key=${API_KEY}`);
  const data = await r.json();
  return (data.documents || []).map(docToObj);
}

async function getDoc(collection, docId) {
  const r = await fetch(`${BASE_URL}/${collection}/${docId}?key=${API_KEY}`);
  if (r.status === 404) return null;
  const data = await r.json();
  return docToObj(data);
}

async function patchDoc(collection, docId, obj) {
  const fields = {};
  for (const k in obj) fields[k] = toFs(obj[k]);
  const r = await fetch(`${BASE_URL}/${collection}/${docId}?key=${API_KEY}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ fields }),
  });
  return r.json();
}

// ===== Routes =====
app.get("/", (req, res) => res.json({ status: "DataPulse backend live" }));
app.get("/health", (req, res) => res.json({ ok: true, ts: Date.now() }));

// ===== AI — Groq API =====
app.post("/api/ai", async (req, res) => {
  try {
    const prompt = req.body.prompt || "Hello";
    const r = await fetch("https://api.groq.com/openai/v1/chat/completions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${process.env.GROQ_API_KEY}`
      },
      body: JSON.stringify({
        model: "openai/gpt-oss-120b",
        messages: [{ role: "user", content: prompt }],
        temperature: 0.7,
        max_tokens: 1024
      })
    });
    const data = await r.json();
    if (data.error) return res.status(500).json({ error: data.error.message });
    const reply = data.choices?.[0]?.message?.content || "No reply";
    res.json({ reply, model: data.model });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

// ===== Admin metrics =====
app.get("/api/admin/metrics", async (req, res) => {
  try {
    const orgs = await listDocs("orgs");
    const contracts = await listDocs("contracts");
    const active = contracts.filter(c => c.status === "active");
    let mrr = 0;
    active.forEach(c => mrr += Number(c.usd || 0));
    res.json({ totalOrgs: orgs.length, activeContracts: active.length, mrrUsd: mrr });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

// ===== Suspend org =====
app.post("/api/admin/suspend-org", async (req, res) => {
  try {
    const { orgId, reason } = req.body;
    if (!orgId) return res.status(400).json({ error: "orgId required" });
    const result = await patchDoc("orgs", orgId, {
      status: "suspended",
      suspendedAt: new Date().toISOString(),
      suspendReason: reason || "",
    });
    res.json({ success: true, result });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

// ===== Extend trial =====
app.post("/api/admin/extend-trial", async (req, res) => {
  try {
    const { orgId, days = 14 } = req.body;
    if (!orgId) return res.status(400).json({ error: "orgId required" });
    const org = await getDoc("orgs", orgId);
    if (!org) return res.status(404).json({ error: "Org not found" });
    const trial = org.trial || {};
    trial.endsAt = new Date(Date.now() + days * 86400000).toISOString();
    trial.paid = false;
    await patchDoc("orgs", orgId, { trial });
    res.json({ success: true });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

// ===== Pipeline =====
app.post("/api/pipeline/run", async (req, res) => {
  res.json({ status: "pipeline ran", ts: Date.now() });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`DataPulse backend on port ${PORT}`));

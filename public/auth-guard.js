// auth-guard.js — Firebase Auth Protection for admin.html
import { initializeApp, getApps } from "https://www.gstatic.com/firebasejs/10.12.0/firebase-app.js";
import { getAuth, signInWithEmailAndPassword, signOut, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/10.12.0/firebase-auth.js";

const firebaseConfig = {
  apiKey: "AIzaSyAb1Fbs8Y36BZ8rnIUZBjocc-m0Em_PgcQ",
  authDomain: "datapulseapp-20237.firebaseapp.com",
  databaseURL: "https://datapulseapp-20237-default-rtdb.europe-west1.firebasedatabase.app",
  projectId: "datapulseapp-20237",
  storageBucket: "datapulseapp-20237.firebasestorage.app",
  messagingSenderId: "459433026519",
  appId: "1:459433026519:web:102f1f951bcb91d306e192"
};

const app = getApps().length ? getApps()[0] : initializeApp(firebaseConfig);
const auth = getAuth(app);

// Show page (remove opacity:0 from <head>)
document.documentElement.style.opacity = '1';

// Create gate overlay
function createGate() {
  if (document.getElementById('agGate')) return;
  const gate = document.createElement('div');
  gate.id = 'agGate';
  gate.style.cssText = `position:fixed;inset:0;z-index:999999;background:#0b0f19;
    display:flex;align-items:center;justify-content:center;padding:20px;
    font-family:Inter,-apple-system,sans-serif;`;
  gate.innerHTML = `
    <div style="background:#111827;border:1px solid #1f2937;border-radius:16px;
      padding:32px 24px;max-width:400px;width:100%;">
      <div style="width:56px;height:56px;border-radius:14px;
        background:linear-gradient(135deg,#10b981,#059669);display:flex;
        align-items:center;justify-content:center;font-size:26px;margin:0 auto 16px;">🔐</div>
      <h2 style="color:#f9fafb;font-size:20px;text-align:center;margin:0 0 6px;font-weight:700;">Admin Login</h2>
      <p style="color:#9ca3af;font-size:13px;text-align:center;margin:0 0 24px;">DataPulse Enterprise · Restricted Access</p>
      <label style="display:block;color:#9ca3af;font-size:12px;margin-bottom:6px;font-weight:600;">Email</label>
      <input id="agEmail" type="email" placeholder="admin@datapulse.et" autocomplete="email"
        style="width:100%;padding:12px 14px;background:#0b0f19;border:1px solid #374151;
        border-radius:8px;color:#f9fafb;font-size:14px;outline:none;box-sizing:border-box;margin-bottom:14px;">
      <label style="display:block;color:#9ca3af;font-size:12px;margin-bottom:6px;font-weight:600;">Password</label>
      <input id="agPassword" type="password" placeholder="••••••••" autocomplete="current-password"
        style="width:100%;padding:12px 14px;background:#0b0f19;border:1px solid #374151;
        border-radius:8px;color:#f9fafb;font-size:14px;outline:none;box-sizing:border-box;margin-bottom:14px;">
      <button id="agBtn" style="width:100%;padding:12px;
        background:linear-gradient(135deg,#10b981,#059669);color:white;border:none;
        border-radius:8px;font-size:14px;font-weight:700;cursor:pointer;">🔓 Sign In</button>
      <div id="agErr" style="background:rgba(239,68,68,0.1);border:1px solid rgba(239,68,68,0.3);
        color:#ef4444;padding:10px;border-radius:8px;font-size:12px;margin-top:12px;display:none;"></div>
      <p style="color:#6b7280;font-size:11px;text-align:center;margin-top:16px;">
        ⚠️ Authorized administrators only. All attempts are logged.</p>
    </div>`;
  document.body.appendChild(gate);

  const btn = gate.querySelector('#agBtn');
  const err = gate.querySelector('#agErr');
  const emailEl = gate.querySelector('#agEmail');
  const passEl = gate.querySelector('#agPassword');

  async function tryLogin() {
    const email = emailEl.value.trim();
    const password = passEl.value;
    if (!email || !password) {
      err.textContent = '⚠️ Email fi password guuti.';
      err.style.display = 'block';
      return;
    }
    btn.disabled = true; btn.textContent = '⏳ Signing in...';
    err.style.display = 'none';
    try {
      await signInWithEmailAndPassword(auth, email, password);
    } catch (e) {
      const msgs = {
        'auth/invalid-email': 'Email dogoggora.',
        'auth/user-not-found': 'User hin argamne.',
        'auth/wrong-password': 'Password dogoggora.',
        'auth/invalid-credential': 'Email ykn password dogoggora.',
        'auth/too-many-requests': 'Yeroo muraasa booda yaali.',
        'auth/network-request-failed': 'Network rakkoo.'
      };
      err.textContent = '❌ ' + (msgs[e.code] || e.message);
      err.style.display = 'block';
    } finally {
      btn.disabled = false; btn.textContent = '🔓 Sign In';
    }
  }
  btn.addEventListener('click', tryLogin);
  passEl.addEventListener('keypress', e => { if (e.key === 'Enter') tryLogin(); });
}

// Sign out button
function addSignOut() {
  if (document.getElementById('agSignOut')) return;
  const b = document.createElement('button');
  b.id = 'agSignOut';
  b.textContent = '🚪 Sign Out';
  b.style.cssText = `position:fixed;bottom:20px;right:20px;z-index:999998;
    padding:8px 14px;background:#1f2937;color:#f9fafb;border:1px solid #374151;
    border-radius:8px;font-size:12px;font-weight:600;cursor:pointer;
    font-family:Inter,sans-serif;`;
  b.onclick = () => { if (confirm('Sign out gochuu barbaadda?')) signOut(auth); };
  document.body.appendChild(b);
}

// Auth state listener
onAuthStateChanged(auth, (user) => {
  const gate = document.getElementById('agGate');
  if (user) {
    if (gate) gate.remove();
    addSignOut();
  } else {
    const so = document.getElementById('agSignOut');
    if (so) so.remove();
    if (!gate) createGate();
  }
});

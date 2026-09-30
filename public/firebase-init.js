import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.0/firebase-app.js";
import { getFirestore, collection, getDocs } from "https://www.gstatic.com/firebasejs/10.12.0/firebase-firestore.js";

const firebaseConfig = {
  apiKey: "AIzaSyAb1Fbs8Y36BZ8rnIUZBjocc-m0Em_PgcQ",
  authDomain: "datapulseapp-20237.firebaseapp.com",
  projectId: "datapulseapp-20237",
  storageBucket: "datapulseapp-20237.firebasestorage.app",
  messagingSenderId: "459433026519",
  appId: "1:459433026519:web:102f1f951bcb91d306e192",
  measurementId: "G-RFN5ZZTE6W"
};

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

let panelEl = null;
function log(msg) {
  console.log(msg);
  if (!panelEl) {
    panelEl = document.createElement('div');
    panelEl.id = 'fsDebugPanel';
    panelEl.style.cssText = 'position:fixed;top:50px;right:8px;z-index:99999;background:#000;color:#0f0;font-family:monospace;font-size:10px;padding:6px 8px;border-radius:6px;border:1px solid #0f0;max-width:260px;max-height:35vh;overflow-y:auto;white-space:pre-wrap;cursor:pointer;';
    panelEl.onclick = () => panelEl.remove();
    document.body.appendChild(panelEl);
  }
  panelEl.textContent += '\n' + msg;
}

// Values nui jijjiiruu barbaadnu
let NEW_VALUES = null; // { sales: '1,130,000', cost: '0', profit: '1,130,000' }
let REPLACE_COUNT = 0;

function replaceAllInDom(oldStr, newStr) {
  if (oldStr === newStr) return 0;
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null);
  let count = 0;
  let n;
  const nodes = [];
  while ((n = walker.nextNode())) {
    if (n.nodeValue && n.nodeValue.indexOf(oldStr) !== -1) {
      nodes.push(n);
    }
  }
  nodes.forEach(node => {
    node.nodeValue = node.nodeValue.split(oldStr).join(newStr);
    count++;
  });
  return count;
}

function doReplace() {
  if (!NEW_VALUES) return 0;
  let total = 0;
  // KPI dashboard dursee
  total += replaceAllInDom('1,147,500', NEW_VALUES.sales);
  total += replaceAllInDom('845,700', NEW_VALUES.cost);
  total += replaceAllInDom('301,800', NEW_VALUES.profit);
  // KPI dabalataa (fallback)
  total += replaceAllInDom('1,147,500', NEW_VALUES.sales);
  return total;
}

// ============================================
// MUTATION OBSERVER — yeroo hunda monitor godhi
// ============================================
function startObserver() {
  if (!NEW_VALUES) return;
  const observer = new MutationObserver(() => {
    const c = doReplace();
    if (c > 0) REPLACE_COUNT += c;
  });
  observer.observe(document.body, {
    childList: true,
    subtree: true,
    characterData: true
  });
  // Ammas yeroo yeroon yaa li (observer miss gochuu danda'a)
  setInterval(() => {
    const c = doReplace();
    if (c > 0) REPLACE_COUNT += c;
  }, 800);
}

// ============================================
// FIRE — data Firestore irraa fida
// ============================================
async function patchKpi() {
  try {
    log('⏳ Loading...');
    const snap = await getDocs(collection(db, "sales"));
    
    let sales = 0, cost = 0, count = 0;
    snap.forEach(d => {
      const v = d.data();
      sales += Number(v.revenue) || Number(v.price) || 0;
      cost += Number(v.cost) || 0;
      count++;
    });
    const profit = sales - cost;

    NEW_VALUES = {
      sales: sales.toLocaleString('en-US'),
      cost: cost.toLocaleString('en-US'),
      profit: profit.toLocaleString('en-US')
    };

    log('📊 Loaded ' + count + ' rows');
    log('🎯 Target: GS=' + NEW_VALUES.sales + ' NP=' + NEW_VALUES.profit);

    // Jalqaba replace yaali
    const first = doReplace();
    REPLACE_COUNT += first;
    log('🔧 First replace: ' + first);

    // Observer jalqabi
    startObserver();
    log('👁️ Observer started');

    // Panel sun 20s booda haqa (yeroo dheeraaf hojjechiisuuf)
    setTimeout(() => {
      if (panelEl) { panelEl.remove(); panelEl = null; }
    }, 20000);
  } catch (e) {
    log('❌ ' + e.message);
  }
}

// ============================================
// RUN
// ============================================
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => setTimeout(patchKpi, 1500));
} else {
  setTimeout(patchKpi, 1500);
}

import os, re

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    content = f.read()

# 1. Universal fix: yeroo login tuqtu, #app fi #main lamaanuu mul'achuu
fix = '''
// ========== APP VISIBILITY FIX ==========
function showAppNow() {
  try {
    var app = document.getElementById('app');
    var main = document.getElementById('main');
    var dash = document.getElementById('dashboard');
    var ls = document.getElementById('loginScreen');
    var lp = document.getElementById('landingPage');
    
    if (app) { app.classList.remove('hidden'); app.style.display = ''; app.removeAttribute('hidden'); }
    if (main) { main.classList.remove('hidden'); main.style.display = ''; main.removeAttribute('hidden'); }
    if (dash) { dash.classList.remove('hidden'); dash.style.display = ''; dash.removeAttribute('hidden'); }
    if (ls) ls.classList.add('hidden');
    if (lp) lp.classList.add('hidden');
    
    // State mirkaneessi
    if (typeof state !== 'undefined') {
      if (!state.tab) state.tab = 'dashboard';
      if (!state.org) state.org = {id: 'ORG-DEMO', name: 'Demo Enterprise'};
      if (!Array.isArray(state.records)) state.records = [];
    }
    
    // Render hojjedhu
    if (typeof render === 'function') {
      try { render(); } catch(e) { console.warn('render err:', e.message); }
    }
  } catch(e) { console.warn('showAppNow error:', e.message); }
}

// Yeroo login/demo tuqtu, ofumaan hojjedhu
document.addEventListener('click', function(ev) {
  var t = ev.target.closest('button, a');
  if (!t) return;
  var txt = (t.textContent || '').trim().toLowerCase();
  if (txt.indexOf('quick demo login') !== -1 || txt === 'log in' || txt === 'sign in') {
    setTimeout(showAppNow, 500);
    setTimeout(showAppNow, 1500);
    setTimeout(showAppNow, 3000);
  }
}, true);

// Yeroo app banamu
window.addEventListener('load', function() {
  setTimeout(function() {
    var app = document.getElementById('app');
    if (app && !app.classList.contains('hidden')) showAppNow();
  }, 1000);
});
// =========================================
'''

if 'APP VISIBILITY FIX' not in content:
    content = content.replace(
        "window.addEventListener('DOMContentLoaded'",
        fix + "\nwindow.addEventListener('DOMContentLoaded'",
        1
    )
    print("✅ APP VISIBILITY FIX dabalameera!")

# 2. render() function keessatti #app hidden haquu
content = content.replace(
    "if (!el) return;\n  \n  try { if (!state.tab) state.tab = 'dashboard'; } catch(e){}",
    "if (!el) return;\n  \n  // #app fi #dashboard hidden haquu\n  try { var _a = document.getElementById('app'); if (_a) { _a.classList.remove('hidden'); _a.style.display = ''; } } catch(e){}\n  try { var _d = document.getElementById('dashboard'); if (_d) { _d.classList.remove('hidden'); _d.style.display = ''; } } catch(e){}\n  try { if (!state.tab) state.tab = 'dashboard'; } catch(e){}"
)

with open(html_path, 'w') as f:
    f.write(content)

print("✅ render() keessatti #app hidden haquu dabalameera!")
print("📍 Hojii xumurameera!")

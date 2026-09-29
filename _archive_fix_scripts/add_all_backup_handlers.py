import os, re

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    content = f.read()

print("=" * 60)
print("🔧 BACKUP HANDLERS DABALUU")
print("=" * 60)

# ============================================================
# 1. HANDLERS HUNDA - code tokko keessatti
# ============================================================
all_handlers = '''
// ============================================================
// ========== BACKUP HANDLERS (UNIVERSAL) ====================
// ============================================================

// ========== AUTH BACKUP HANDLER ==========
document.addEventListener('click', function(ev) {
  var t = ev.target.closest('button, a');
  if (!t) return;
  var txt = (t.textContent || '').trim().toLowerCase();
  var id = t.id || '';
  
  // Register Org
  if (id === 'tbRegister' || txt.indexOf('register org') !== -1) {
    ev.preventDefault();
    try {
      var lf = document.getElementById('loginForm'); if (lf) lf.classList.add('hidden');
      var rf = document.getElementById('regForm'); if (rf) rf.classList.remove('hidden');
    } catch(e) { console.warn('reg err:', e.message); }
    return;
  }
  // Sign In tab
  if (id === 'tbLogin' && txt === 'sign in') {
    try {
      var lf2 = document.getElementById('loginForm'); if (lf2) lf2.classList.remove('hidden');
      var rf2 = document.getElementById('regForm'); if (rf2) rf2.classList.add('hidden');
    } catch(e) {}
    return;
  }
}, true);

// ========== UNIVERSAL BUTTON HANDLER ==========
document.addEventListener('click', function(ev) {
  var t = ev.target.closest('button, a');
  if (!t) return;
  var txt = (t.textContent || '').trim().toLowerCase();
  
  // Quick Demo Login
  if (txt.indexOf('quick demo login') !== -1 || txt.indexOf('demo login') !== -1) {
    ev.preventDefault();
    if (typeof quickDemoLogin === 'function') quickDemoLogin();
    return;
  }
  
  // Log In button
  if (txt === 'log in' && t.tagName === 'BUTTON') {
    var lf = document.getElementById('loginForm');
    if (lf && typeof lf.requestSubmit === 'function') {
      ev.preventDefault();
      lf.requestSubmit();
    }
    return;
  }
}, true);

// ========== LAUNCH BUTTON HANDLER ==========
document.addEventListener('click', function(ev) {
  var t = ev.target.closest('button, a');
  if (!t) return;
  var txt = (t.textContent || '').trim().toLowerCase();
  
  // Launch App button
  if (txt.indexOf('launch app') !== -1) {
    ev.preventDefault();
    try {
      var lp = document.getElementById('landingPage'); if (lp) lp.classList.add('hidden');
      var ls = document.getElementById('loginScreen');
      if (ls) { ls.classList.remove('hidden'); ls.classList.add('flex'); }
      else {
        var app = document.getElementById('app'); if (app) { app.classList.remove('hidden'); app.style.display = ''; }
      }
    } catch(e) { console.warn('launch err:', e.message); }
    return;
  }
  
  // Start Free Trial, See Features (landing page buttons)
  if (txt.indexOf('start free trial') !== -1 || txt.indexOf('see features') !== -1) {
    ev.preventDefault();
    try {
      var lp2 = document.getElementById('landingPage'); if (lp2) lp2.classList.add('hidden');
      var ls2 = document.getElementById('loginScreen');
      if (ls2) { ls2.classList.remove('hidden'); ls2.classList.add('flex'); }
    } catch(e) {}
    return;
  }
}, true);

// ========== APP VISIBILITY HANDLER ==========
function forceShowApp() {
  try {
    ['app', 'main'].forEach(function(id) {
      var el = document.getElementById(id);
      if (el) { el.classList.remove('hidden'); el.style.display = ''; el.removeAttribute('hidden'); }
    });
    var ls = document.getElementById('loginScreen'); if (ls) ls.classList.add('hidden');
    var lp = document.getElementById('landingPage'); if (lp) lp.classList.add('hidden');
    if (typeof state !== 'undefined') {
      if (!state.tab) state.tab = 'dashboard';
      if (!state.org) state.org = {id: 'ORG-DEMO', name: 'Demo Enterprise'};
      if (!state.user) state.user = {name: 'Demo Admin', email: 'demo@datapulse.com', role: 'admin'};
      if (!Array.isArray(state.records)) state.records = [];
    }
    if (typeof render === 'function') {
      try { render(); } catch(e) { console.warn('render err:', e.message); }
    }
  } catch(e) { console.warn('forceShowApp err:', e.message); }
}

// Yeroo app banamu fi login tuqtu
window.addEventListener('load', function() {
  setTimeout(function() {
    var app = document.getElementById('app');
    if (app && !app.classList.contains('hidden')) forceShowApp();
  }, 800);
});

document.addEventListener('click', function(ev) {
  var t = ev.target.closest('button');
  if (!t) return;
  var txt = (t.textContent || '').trim().toLowerCase();
  if (txt.indexOf('quick demo login') !== -1 || txt === 'log in') {
    setTimeout(forceShowApp, 800);
    setTimeout(forceShowApp, 2000);
  }
}, true);

// ============================================================
'''

# ============================================================
# 2. Handlers dabalii - script tag keessatti
# ============================================================
if 'BACKUP HANDLERS (UNIVERSAL)' not in content:
    # Bakka </script> isa dhumaa barbaadi
    last_script_close = content.rfind('</script>')
    
    if last_script_close > 0:
        # Handlers galchi - </script> dura
        content = content[:last_script_close] + all_handlers + '\n' + content[last_script_close:]
        print("✅ Handlers hunni dabalameera (</script> dura)")
    else:
        print("❌ </script> hin argamne!")
else:
    print("⚠️  Handlers amma jiru.")

with open(html_path, 'w') as f:
    f.write(content)

# ============================================================
# 3. Mirkaneessi
# ============================================================
with open(html_path, 'r') as f:
    new_content = f.read()

print("\n" + "=" * 60)
print("📍 MIRKANEESSA")
print("=" * 60)

handlers = [
    'AUTH BACKUP HANDLER',
    'UNIVERSAL BUTTON HANDLER',
    'LAUNCH BUTTON HANDLER',
    'APP VISIBILITY HANDLER',
    'BACKUP HANDLERS (UNIVERSAL)',
]

for h in handlers:
    if h in new_content:
        idx = new_content.find(h)
        line_no = new_content[:idx].count('\n') + 1
        print(f"   ✅ {h} (Sarara {line_no})")
    else:
        print(f"   ❌ {h} hin jiru")

# Script balance
opens = len(re.findall(r'<script\b[^>]*>', new_content))
closes = new_content.count('</script>')
print(f"\n   <script>: {opens}, </script>: {closes}, Diff: {opens - closes}")

print("\n" + "=" * 60)
print("✅ XUMURAMEERA!")
print("=" * 60)

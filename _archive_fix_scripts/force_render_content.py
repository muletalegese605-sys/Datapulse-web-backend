import os, re

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    content = f.read()

# 1. Yeroo dashboard banamu, render() function hojjechuu fi content guutuu mirkaneessi
force_render = '''
// ========== FORCE RENDER CONTENT ==========
window.addEventListener('load', function() {
  setTimeout(function() {
    try {
      // Yoo dashboard fi app mul'atan, render() hojjedhu
      var d = document.getElementById('dashboard');
      var a = document.getElementById('app');
      if ((d && !d.classList.contains('hidden')) || (a && !a.classList.contains('hidden'))) {
        if (typeof render === 'function') {
          try { render(); } catch(e) { console.warn('Render error:', e.message); }
        }
      }
    } catch(e) {}
  }, 1500);
});

// Yeroo login tuqtu, render() dabaluu
document.addEventListener('click', function(ev) {
  var t = ev.target.closest('button, a');
  if (!t) return;
  var txt = (t.textContent || '').trim().toLowerCase();
  if (txt.indexOf('quick demo login') !== -1 || txt === 'log in' || txt === 'sign in') {
    setTimeout(function() {
      try {
        if (typeof render === 'function') render();
      } catch(e) { console.warn('Post-login render error:', e.message); }
    }, 1200);
  }
}, true);
// =============================================
'''

if 'FORCE RENDER CONTENT' not in content:
    content = content.replace(
        "window.addEventListener('DOMContentLoaded'",
        force_render + "\nwindow.addEventListener('DOMContentLoaded'",
        1
    )
    print("✅ Force render content dabalameera!")

# 2. state.records ramaduu hundi, walitti bu'iinsa dhorkuuf - 'var' fayyadami
# Kun state.records sun hunda waliin akka hojjetu godha
content = content.replace('state.records = this._cache.records;', 'state.records = this._cache.records || [];')

with open(html_path, 'w') as f:
    f.write(content)

print("📍 Hojii xumurameera!")

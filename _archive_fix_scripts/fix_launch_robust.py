import os, re

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    content = f.read()

# 1. Button "Launch App" fi "Sign In" tiif type="button" dabaluu
content = re.sub(
    r'(<button\s+)(onclick="showLoginFromLanding\(\)")',
    r'\1type="button" \2',
    content
)

# 2. Function showLoginFromLanding sirreessuu
old_fn = '''function showLoginFromLanding(){
  document.getElementById('landingPage').classList.add('hidden');
  const ls = document.getElementById('loginScreen');
  ls.classList.remove('hidden'); ls.classList.add('flex');
}'''

new_fn = '''function showLoginFromLanding(){
  try {
    var lp = document.getElementById('landingPage');
    if (lp) lp.classList.add('hidden');
    var ls = document.getElementById('loginScreen');
    if (ls) {
      ls.classList.remove('hidden');
      ls.classList.add('flex');
    } else {
      var app = document.getElementById('app');
      if (app) app.classList.remove('hidden');
      if (typeof go === 'function') go('dashboard');
    }
  } catch(e) {
    console.warn('Launch failed:', e.message);
    var app = document.getElementById('app');
    if (app) app.classList.remove('hidden');
    if (typeof go === 'function') go('dashboard');
    else if (typeof render === 'function') render();
  }
}'''

if old_fn in content:
    content = content.replace(old_fn, new_fn)
    print("✅ Function 'showLoginFromLanding' sirreeffameera!")
else:
    print("⚠️ Function duraa hin argamne. Koodii harkaan ilaali.")

# 3. Global event listener dabaluu (backup)
backup_listener = '''
// ========== LAUNCH BUTTON BACKUP ==========
document.addEventListener('click', function(ev) {
  var btn = ev.target.closest('button');
  if (!btn) return;
  var txt = btn.textContent.trim();
  if (txt.indexOf('Launch App') !== -1 || txt.indexOf('Start Free Trial') !== -1) {
    ev.preventDefault();
    if (typeof showLoginFromLanding === 'function') showLoginFromLanding();
  }
});
// ==========================================
'''

if 'LAUNCH BUTTON BACKUP' not in content:
    if '// ========== BACKEND API INTEGRATION ==========' in content:
        content = content.replace(
            '// ========== BACKEND API INTEGRATION ==========',
            backup_listener + '\n// ========== BACKEND API INTEGRATION ==========',
            1
        )
    else:
        content = content.replace(
            'window.addEventListener(\'DOMContentLoaded\'',
            backup_listener + '\nwindow.addEventListener(\'DOMContentLoaded\'',
            1
        )
    print("✅ Backup event listener dabalameera!")

with open(html_path, 'w') as f:
    f.write(content)

print("📍 Hojii xumurameera!")

import os, re

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    content = f.read()

changes = []

# ============================================================
# 1. showLoginFromLanding function sirreessi (nageenya qabu)
# ============================================================
old_fn = r'function\s+showLoginFromLanding\s*\(\s*\)\s*\{[\s\S]*?\n\}'

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
      if (app) { app.classList.remove('hidden'); app.style.display = ''; }
      if (typeof go === 'function') go('dashboard');
    }
  } catch(e) {
    console.warn('showLoginFromLanding error:', e.message);
    var app = document.getElementById('app');
    if (app) { app.classList.remove('hidden'); app.style.display = ''; }
  }
}'''

if re.search(old_fn, content):
    content = re.sub(old_fn, new_fn, content, count=1)
    changes.append('showLoginFromLanding function sirreeffameera')

# ============================================================
# 2. quickDemoLogin function dabalii
# ============================================================
if 'function quickDemoLogin' not in content:
    demo_fn = '''
function quickDemoLogin() {
  try {
    localStorage.setItem('dp_demo_user', JSON.stringify({name:'Demo Admin', email:'demo@datapulse.com', role:'admin'}));
    var ls = document.getElementById('loginScreen');
    if (ls) ls.classList.add('hidden');
    var lp = document.getElementById('landingPage');
    if (lp) lp.classList.add('hidden');
    var app = document.getElementById('app');
    if (app) { app.classList.remove('hidden'); app.style.display = ''; }
    var main = document.getElementById('main');
    if (main) {
      main.classList.remove('hidden');
      main.style.display = '';
    }
    if (typeof state !== 'undefined') {
      state.user = {name: 'Demo Admin', email: 'demo@datapulse.com', role: 'admin'};
      state.org = {id: 'ORG-DEMO', name: 'Demo Enterprise'};
      if (!state.tab) state.tab = 'dashboard';
      if (!Array.isArray(state.records)) state.records = [];
    }
    if (typeof render === 'function') render();
    if (typeof toast === 'function') toast('Demo login successful', 'success');
  } catch(e) { console.warn('quickDemoLogin error:', e.message); }
}
'''
    # Bakka window.addEventListener('DOMContentLoaded') dura galchi
    if "window.addEventListener('DOMContentLoaded'" in content:
        content = content.replace(
            "window.addEventListener('DOMContentLoaded'",
            demo_fn + "\nwindow.addEventListener('DOMContentLoaded'",
            1
        )
    else:
        content = content.replace('</script>', demo_fn + '\n</script>', 1)
    changes.append('quickDemoLogin function dabalameera')

# ============================================================
# 3. Button "Launch App" onclick sirreessi - inline JS
# ============================================================
inline_js = "event.preventDefault();try{var lp=document.getElementById('landingPage');if(lp)lp.classList.add('hidden');var ls=document.getElementById('loginScreen');if(ls){ls.classList.remove('hidden');ls.classList.add('flex');}else{var app=document.getElementById('app');if(app){app.classList.remove('hidden');app.style.display='';}}}catch(e){alert('Launch error: '+e.message)}"

def fix_launch_btn(m):
    tag = m.group(0)
    tag = re.sub(r'\s*onclick="[^"]*"', '', tag)
    tag = tag.replace('<button', '<button type="button" onclick="' + inline_js + '"', 1)
    return tag

content, n = re.subn(
    r'<button[^>]*>[\s\S]{0,200}?Launch App[\s\S]{0,30}?</button>',
    fix_launch_btn,
    content
)
if n > 0:
    changes.append(f'Button "Launch App" {n} sirreeffameera')

# ============================================================
# 4. Quick Demo Login button onclick sirreessi
# ============================================================
def fix_demo_btn(m):
    tag = m.group(0)
    tag = re.sub(r'\s*onclick="[^"]*"', '', tag)
    tag = tag.replace('<button', '<button type="button" onclick="quickDemoLogin()"', 1)
    return tag

content, n = re.subn(
    r'<button[^>]*>[\s\S]{0,200}?Quick Demo Login[\s\S]{0,30}?</button>',
    fix_demo_btn,
    content
)
if n > 0:
    changes.append(f'Button "Quick Demo Login" {n} sirreeffameera')

# ============================================================
# 5. Register Org fi Sign In buttons sirreessi (backup handler)
# ============================================================
backup_handler = '''
// ========== BACKUP BUTTON HANDLER ==========
document.addEventListener('click', function(ev) {
  var t = ev.target.closest('button');
  if (!t) return;
  var txt = (t.textContent || '').trim().toLowerCase();
  var id = t.id || '';
  
  // Launch App
  if (txt.indexOf('launch app') !== -1 && !t.getAttribute('onclick')) {
    ev.preventDefault();
    try {
      var lp = document.getElementById('landingPage'); if (lp) lp.classList.add('hidden');
      var ls = document.getElementById('loginScreen');
      if (ls) { ls.classList.remove('hidden'); ls.classList.add('flex'); }
      else { var app = document.getElementById('app'); if (app) { app.classList.remove('hidden'); app.style.display = ''; } }
    } catch(e) {}
  }
  
  // Quick Demo Login
  if (txt.indexOf('quick demo login') !== -1) {
    ev.preventDefault();
    if (typeof quickDemoLogin === 'function') quickDemoLogin();
  }
  
  // Register Org
  if (id === 'tbRegister' || txt.indexOf('register org') !== -1) {
    ev.preventDefault();
    if (typeof switchAuth === 'function') switchAuth('register');
  }
  
  // Sign In tab
  if (id === 'tbLogin' && txt === 'sign in') {
    if (typeof switchAuth === 'function') switchAuth('login');
  }
});
// ==========================================
'''

if 'BACKUP BUTTON HANDLER' not in content:
    if 'window.addEventListener(\'DOMContentLoaded\'' in content:
        content = content.replace(
            "window.addEventListener('DOMContentLoaded'",
            backup_handler + "\nwindow.addEventListener('DOMContentLoaded'",
            1
        )
        changes.append('Backup button handler dabalameera')

# ============================================================
# 6. Global error catcher - visible alert (yeroo rakkoo mudate)
# ============================================================
if 'window.__dp_error_shown' not in content:
    error_catcher = '''
window.__dp_error_shown = false;
window.addEventListener('error', function(e) {
  if (!window.__dp_error_shown) {
    window.__dp_error_shown = true;
    console.error('DP Error:', e.message, 'at', e.filename, ':', e.lineno);
  }
});
'''
    if "window.addEventListener('DOMContentLoaded'" in content:
        content = content.replace(
            "window.addEventListener('DOMContentLoaded'",
            error_catcher + "\nwindow.addEventListener('DOMContentLoaded'",
            1
        )
        changes.append('Global error catcher dabalameera')

# ============================================================
# Save
# ============================================================
with open(html_path, 'w') as f:
    f.write(content)

print("=" * 60)
print("✅ FIX XUMURAMEERA!")
print("=" * 60)
for c in changes:
    print("  • " + c)
if not changes:
    print("  ⚠️  Wanti jijjiirame hin jiru.")
print("=" * 60)

# Sanada mirkaneessi
with open(html_path, 'r') as f:
    new_content = f.read()

print("\n📍 MIRKANEESSA:")
print(f"  quickDemoLogin function: {'✅' if 'function quickDemoLogin' in new_content else '❌'}")
print(f"  BACKUP BUTTON HANDLER: {'✅' if 'BACKUP BUTTON HANDLER' in new_content else '❌'}")
print(f"  inline onclick Launch: {'✅' if 'Launch error' in new_content else '❌'}")

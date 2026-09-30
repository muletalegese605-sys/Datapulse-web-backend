import os, re

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    content = f.read()

changes = []

# 1. Button tbRegister: barruu "Register Org" dabaluu
old_reg = r'<button id="tbRegister" onclick="switchAuth(\\?\'register\\?\')"></button>'
new_reg = '<button id="tbRegister" onclick="switchAuth(\'register\')" class="py-2.5 rounded-xl text-xs font-bold text-slate-400 hover:text-emerald-400 transition" data-i18n="registerOrg">Register Org</button>'

if 'data-i18n="registerOrg">Register Org</button>' not in content:
    # Regex: button tbRegister kan barruu hin qabne barbaadi
    pattern = re.compile(
        r'<button\s+id="tbRegister"[^>]*>\s*</button>',
        re.IGNORECASE
    )
    match = pattern.search(content)
    if match:
        content = content[:match.start()] + new_reg + content[match.end():]
        changes.append('Button tbRegister: barruu "Register Org" dabalameera')
    else:
        # Yoo button sun hin jiraanne, dura button tbLogin booda galchi
        m2 = re.search(r'<button\s+id="tbLogin"[^>]*>.*?</button>', content, re.DOTALL | re.IGNORECASE)
        if m2:
            content = content[:m2.end()] + '\n                ' + new_reg + content[m2.end():]
            changes.append('Button tbRegister haaraa dabalameera')
        else:
            changes.append('⚠️ Button tbLogin hin argamne')

# 2. switchAuth function sirreessuu (yoo hin jiraanne dabalii)
if 'function switchAuth' not in content:
    fn = '''
function switchAuth(mode) {
  try {
    var tbL = document.getElementById('tbLogin');
    var tbR = document.getElementById('tbRegister');
    var regForm = document.getElementById('regForm');
    var loginForm = document.getElementById('loginForm');
    
    if (mode === 'register') {
      if (tbR) { tbR.className = 'py-2.5 rounded-xl text-xs font-bold bg-emerald-500 text-slate-950'; }
      if (tbL) { tbL.className = 'py-2.5 rounded-xl text-xs font-bold text-slate-400 hover:text-emerald-400 transition'; }
      if (regForm) regForm.classList.remove('hidden');
      if (loginForm) loginForm.classList.add('hidden');
    } else {
      if (tbL) { tbL.className = 'py-2.5 rounded-xl text-xs font-bold bg-emerald-500 text-slate-950'; }
      if (tbR) { tbR.className = 'py-2.5 rounded-xl text-xs font-bold text-slate-400 hover:text-emerald-400 transition'; }
      if (loginForm) loginForm.classList.remove('hidden');
      if (regForm) regForm.classList.add('hidden');
    }
  } catch(e) { console.warn('switchAuth error:', e.message); }
}

'''
    content = content.replace("window.addEventListener('DOMContentLoaded'", fn + "window.addEventListener('DOMContentLoaded'", 1)
    changes.append('Function switchAuth dabalameera')

# 3. Backup handler: buttons lamaanuu hojjechuuf
backup = '''
// ========== AUTH BACKUP HANDLER ==========
document.addEventListener('click', function(ev) {
  var t = ev.target.closest('button');
  if (!t) return;
  var id = t.id || '';
  var txt = (t.textContent || '').trim().toLowerCase();
  if (id === 'tbRegister' || txt.indexOf('register org') !== -1) {
    ev.preventDefault();
    if (typeof switchAuth === 'function') switchAuth('register');
  } else if (id === 'tbLogin' || txt === 'sign in') {
    if (typeof switchAuth === 'function') switchAuth('login');
  } else if (txt.indexOf('quick demo login') !== -1) {
    ev.preventDefault();
    if (typeof quickDemoLogin === 'function') quickDemoLogin();
  }
});
// ==========================================
'''
if 'AUTH BACKUP HANDLER' not in content:
    content = content.replace("window.addEventListener('DOMContentLoaded'", backup + "\nwindow.addEventListener('DOMContentLoaded'", 1)
    changes.append('Backup handler dabalameera')

with open(html_path, 'w') as f:
    f.write(content)

print("=" * 50)
print("✅ Hojii xumurameera!")
for c in changes:
    print("  • " + c)
if not changes:
    print("  ⚠️ Wanti jijjiirame hin jiru.")
print("=" * 50)

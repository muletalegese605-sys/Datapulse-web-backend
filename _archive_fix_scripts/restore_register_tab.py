import os, re

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    content = f.read()

changes = []

# ================================================================
# 1. TAB CONTAINER: Sign In + Register Org
# ================================================================
if 'tbRegister' not in content:
    # Bakka "Sign In" button jiru barbaadi
    m = re.search(
        r'(<button[^>]*>)\s*(?:<[^>]*>\s*)*Sign In\s*(?:</[^>]*>\s*)*(</button>)',
        content, re.IGNORECASE | re.DOTALL
    )
    
    if m:
        # Button isa duraa (Sign In) guutuu argadhu
        start = m.start()
        end = m.end()
        
        # Sign In button guutuu
        signin_btn = content[start:end]
        
        # Register Org button qopheessi (Sign In waliin fakkaachuu qabu)
        reg_btn = '''<button id="tbRegister" onclick="switchAuth('register')" class="flex-1 py-2.5 rounded-xl text-xs font-bold text-slate-400 hover:text-emerald-400 transition" data-i18n="registerOrg">Register Org</button>'''
        
        # Sign In button keessatti "flex-1" jiraachuu qaba - yoo hin jiraanne dabaluu
        if 'flex-1' not in signin_btn:
            signin_btn = signin_btn.replace('class="', 'class="flex-1 ', 1)
        
        # Bakka galchi
        content = content[:start] + signin_btn + '\n                ' + reg_btn + content[end:]
        changes.append('Register Org tab deebi\'ee galmeeffame')
    else:
        changes.append('⚠️ Button "Sign In" hin argamne')

# ================================================================
# 2. ONCLICK HANDLERS: hunda sirreessi
# ================================================================
# Sign In tab
content = re.sub(
    r'(<button[^>]*>)\s*(?:<[^>]*>\s*)*Sign In\s*(?:</[^>]*>\s*)*(</button>)',
    lambda m: m.group(0).replace('<button', '<button onclick="switchAuth(\'signin\')"', 1) if 'onclick' not in m.group(0) else m.group(0),
    content, count=1, flags=re.IGNORECASE | re.DOTALL
)

# Register Org tab - yoo onclick hin qabu
content = re.sub(
    r'(<button\s+id="tbRegister"[^>]*?)(?:\s+onclick="[^"]*")?',
    r'\1 onclick="switchAuth(\'register\')"',
    content, count=1
)

# Quick Demo Login - onclick sirreessi
content = re.sub(
    r'(<button[^>]*onclick="[^"]*quickDemo[^"]*"[^>]*>)',
    '<button type="button" onclick="quickDemoLogin()" class="w-full mt-3 py-3 rounded-xl bg-slate-800 border border-slate-700 text-emerald-400 font-bold text-sm hover:bg-slate-700 transition">',
    content, count=1
)

# ================================================================
# 3. FUNCTIONS: quickDemoLogin + switchAuth + showLogin
# ================================================================
if 'function quickDemoLogin' not in content:
    fn = '''
function quickDemoLogin() {
  try {
    localStorage.setItem('dp_demo_user', JSON.stringify({name:'Demo Admin', email:'demo@datapulse.com', role:'admin', org:'ORG-DEMO'}));
    var ls = document.getElementById('loginScreen');
    if (ls) ls.classList.add('hidden');
    var app = document.getElementById('app');
    if (app) { app.classList.remove('hidden'); app.style.display = ''; }
    if (typeof state !== 'undefined') {
      state.user = {name: 'Demo Admin', email: 'demo@datapulse.com', role: 'admin'};
      state.org = {id: 'ORG-DEMO', name: 'Demo Enterprise'};
    }
    if (typeof render === 'function') render();
    if (typeof toast === 'function') toast('Demo login successful', 'success');
  } catch(e) { console.warn('Demo login error:', e.message); }
}

'''
    content = content.replace("window.addEventListener('DOMContentLoaded'", fn + "window.addEventListener('DOMContentLoaded'", 1)
    changes.append('quickDemoLogin function dabalameera')

if 'function switchAuth' not in content:
    fn = '''
function switchAuth(mode) {
  try {
    var ts = document.getElementById('tbSignin');
    var tr = document.getElementById('tbRegister');
    if (ts) ts.className = 'flex-1 py-2.5 rounded-xl text-xs font-bold transition ' + (mode === 'signin' ? 'bg-emerald-500/20 text-emerald-400' : 'text-slate-400 hover:text-emerald-400');
    if (tr) tr.className = 'flex-1 py-2.5 rounded-xl text-xs font-bold transition ' + (mode === 'register' ? 'bg-emerald-500/20 text-emerald-400' : 'text-slate-400 hover:text-emerald-400');
    var loginForm = document.getElementById('loginForm');
    var regForm = document.getElementById('registerForm');
    if (loginForm) loginForm.classList.toggle('hidden', mode !== 'signin');
    if (regForm) regForm.classList.toggle('hidden', mode !== 'register');
  } catch(e) { console.warn('switchAuth error:', e.message); }
}

'''
    content = content.replace("window.addEventListener('DOMContentLoaded'", fn + "window.addEventListener('DOMContentLoaded'", 1)
    changes.append('switchAuth function dabalameera')

# ================================================================
# 4. BACKUP HANDLER: button-wwan hunda hojjechuuf
# ================================================================
backup = '''
// ========== AUTH BACKUP HANDLER ==========
document.addEventListener('click', function(ev) {
  var t = ev.target.closest('button, a');
  if (!t) return;
  var txt = (t.textContent || '').trim().toLowerCase();
  var id = t.id || '';
  
  // Register Org
  if (id === 'tbRegister' || txt.indexOf('register org') !== -1) {
    ev.preventDefault();
    if (typeof switchAuth === 'function') switchAuth('register');
    return;
  }
  // Sign In tab (yeroo tab qofa ta'e, form submit hin godhu)
  if (id === 'tbSignin') {
    if (typeof switchAuth === 'function') switchAuth('signin');
    return;
  }
  // Quick Demo Login
  if (txt.indexOf('quick demo login') !== -1 || txt.indexOf('demo login') !== -1) {
    ev.preventDefault();
    if (typeof quickDemoLogin === 'function') quickDemoLogin();
    return;
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


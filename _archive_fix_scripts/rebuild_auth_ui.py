import os, re

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    content = f.read()

changes = []

# ================================================================
# 1. TAB CONTAINER: Sign In + Register Org
# ================================================================
# Bakka "Sign In" tab jiru barbaadi (button ykn div)
signin_match = re.search(
    r'(<(?:button|div)[^>]*>)\s*(?:<[^>]*>\s*)*\s*(?:Sign In|signIn)\s*(?:</[^>]*>\s*)*',
    content, re.IGNORECASE
)

if signin_match and 'tbRegister' not in content:
    start = signin_match.start()
    # Fuula duraa (container opening) barbaadi - max 300 chars
    container_start = max(0, start - 300)
    prefix = content[container_start:start]
    # <div ...class="..."> banuu barbaadi
    open_div = prefix.rfind('<div')
    if open_div != -1:
        abs_open = container_start + open_div
        # Tab container guutuu bakka buusuu
        # Mudaa: Sign In + Register Org
        new_tabs = '''<div class="flex gap-2 p-1 bg-slate-900/50 rounded-xl mb-4">
            <button id="tbSignin" onclick="switchAuth('signin')" class="flex-1 py-2.5 rounded-xl text-xs font-bold bg-emerald-500/20 text-emerald-400 transition">Sign In</button>
            <button id="tbRegister" onclick="switchAuth('register')" class="flex-1 py-2.5 rounded-xl text-xs font-bold text-slate-400 hover:text-emerald-400 transition" data-i18n="registerOrg">Register Org</button>
        </div>'''
        # Hanga "Sign In" tab xumuraatti haqi
        end_search = content.find('</button>', signin_match.end())
        if end_search == -1:
            end_search = content.find('</div>', signin_match.end())
        if end_search == -1:
            end_search = signin_match.end()
        else:
            end_search = content.find('>', end_search) + 1
        
        content = content[:abs_open] + new_tabs + content[end_search:]
        changes.append('Tab container (Sign In + Register Org) deebi\'ee galmeeffame')

# ================================================================
# 2. QUICK DEMO LOGIN button: bakka "SANDBOX" dura
# ================================================================
if 'quickDemoLogin' not in content or 'data-i18n="quickDemo"' not in content:
    demo_btn = '''<button type="button" onclick="quickDemoLogin()" class="w-full mt-3 py-3 rounded-xl bg-slate-800 border border-slate-700 text-emerald-400 font-bold text-sm hover:bg-slate-700 transition">
            <i class="fa-solid fa-bolt mr-1"></i><span data-i18n="quickDemo">Quick Demo Login</span>
        </button>'''
    
    # Bakka "SANDBOX" jiru barbaadi
    sandbox_match = re.search(r'(<[^>]*>\s*SANDBOX\s*</[^>]*>)', content, re.IGNORECASE)
    if sandbox_match:
        insert_at = sandbox_match.start()
        content = content[:insert_at] + demo_btn + '\n        ' + content[insert_at:]
        changes.append('Quick Demo Login button galmeeffame')
    else:
        # Yoo SANDBOX hin argamne, Log In button booda galchi
        login_match = re.search(r'(<button[^>]*onclick=["\']?[^"\']*[Ll]ogin[^"\']*["\']?[^>]*>.*?</button>)', content, re.DOTALL)
        if login_match:
            insert_at = login_match.end()
            content = content[:insert_at] + '\n        ' + demo_btn + content[insert_at:]
            changes.append('Quick Demo Login button galmeeffame (Log In booda)')

# ================================================================
# 3. FUNCTIONS: quickDemoLogin + switchAuth
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
    if (ts) { ts.className = 'flex-1 py-2.5 rounded-xl text-xs font-bold transition ' + (mode === 'signin' ? 'bg-emerald-500/20 text-emerald-400' : 'text-slate-400 hover:text-emerald-400'); }
    if (tr) { tr.className = 'flex-1 py-2.5 rounded-xl text-xs font-bold transition ' + (mode === 'register' ? 'bg-emerald-500/20 text-emerald-400' : 'text-slate-400 hover:text-emerald-400'); }
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
# 4. BACKUP HANDLER: button-wwan hojjechuuf
# ================================================================
backup = '''
// ========== AUTH BACKUP HANDLER ==========
document.addEventListener('click', function(ev) {
  var t = ev.target.closest('button, a');
  if (!t) return;
  var txt = (t.textContent || '').trim().toLowerCase();
  var id = t.id || '';
  if (id === 'tbRegister' || txt.indexOf('register org') !== -1) {
    ev.preventDefault();
    if (typeof switchAuth === 'function') switchAuth('register');
  }
  if (id === 'tbSignin' || txt === 'sign in' && t.tagName === 'BUTTON') {
    if (typeof switchAuth === 'function') switchAuth('signin');
  }
  if (txt.indexOf('quick demo login') !== -1 || txt.indexOf('demo login') !== -1) {
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
    print("  ⚠️ Wanti jijjiirame hin jiru. Koodii harkaan ilaaluu qabna.")
print("=" * 50)


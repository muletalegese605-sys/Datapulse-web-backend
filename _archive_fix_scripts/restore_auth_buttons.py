import os, re

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    content = f.read()

changes = []

# 1. Register Org tab deebisuu
if 'id="tbRegister"' not in content:
    m = re.search(r'(<button[^>]*>[\s\S]{0,300}?Sign In[\s\S]{0,100}?</button>)', content)
    if m:
        signin_btn = m.group(1)
        cls_match = re.search(r'class="([^"]*)"', signin_btn)
        cls = cls_match.group(1) if cls_match else ''
        reg_cls = 'py-2.5 rounded-xl text-xs font-bold text-slate-400'
        reg_btn = f'\n            <button id="tbRegister" onclick="switchAuth(\'register\')" class="{reg_cls}" data-i18n="registerOrg">Register Org</button>'
        idx = content.find(signin_btn) + len(signin_btn)
        content = content[:idx] + reg_btn + content[idx:]
        changes.append('Register Org tab restored')

# 2. Quick Demo Login button deebisuu
if 'Quick Demo Login' not in content:
    m = re.search(r'(<button[^>]*>[\s\S]{0,300}?Log In[\s\S]{0,100}?</button>)', content)
    if m:
        login_btn = m.group(1)
        demo_btn = '''

        <button type="button" onclick="quickDemoLogin()" class="w-full mt-3 py-3 rounded-xl bg-slate-800 border border-slate-700 text-emerald-400 font-bold text-sm">
          <i class="fa-solid fa-bolt mr-1"></i><span data-i18n="quickDemo">Quick Demo Login</span>
        </button>'''
        idx = content.find(login_btn) + len(login_btn)
        content = content[:idx] + demo_btn + content[idx:]
        changes.append('Quick Demo Login button restored')

# 3. quickDemoLogin function dabalii
if 'function quickDemoLogin' not in content:
    fn = '''
function quickDemoLogin() {
  try {
    var ls = document.getElementById('loginScreen');
    if (ls) ls.classList.add('hidden');
    var app = document.getElementById('app');
    if (app) app.classList.remove('hidden');
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
    changes.append('quickDemoLogin function added')

# 4. switchAuth function dabalii (yoo hin jiraanne)
if 'function switchAuth' not in content:
    fn = '''
function switchAuth(mode) {
  try {
    var tabs = document.querySelectorAll('[id^="tb"]');
    tabs.forEach(function(t){
      t.classList.remove('bg-emerald-500/20','text-emerald-400','border-emerald-500/50','text-white');
      t.classList.add('text-slate-400');
    });
    var target = document.getElementById('tb' + mode.charAt(0).toUpperCase() + mode.slice(1));
    if (target) {
      target.classList.remove('text-slate-400');
      target.classList.add('bg-emerald-500/20','text-emerald-400');
    }
    if (mode === 'register') {
      document.querySelectorAll('[id*="loginForm"], [id*="LoginForm"]').forEach(function(f){ f.classList.add('hidden'); });
      document.querySelectorAll('[id*="registerForm"], [id*="RegisterForm"]').forEach(function(f){ f.classList.remove('hidden'); });
    } else {
      document.querySelectorAll('[id*="registerForm"], [id*="RegisterForm"]').forEach(function(f){ f.classList.add('hidden'); });
      document.querySelectorAll('[id*="loginForm"], [id*="LoginForm"]').forEach(function(f){ f.classList.remove('hidden'); });
    }
  } catch(e) { console.warn('switchAuth error:', e.message); }
}

'''
    content = content.replace("window.addEventListener('DOMContentLoaded'", fn + "window.addEventListener('DOMContentLoaded'", 1)
    changes.append('switchAuth function added')

# 5. Global backup handler (hundi hojjechuuf)
backup = '''
// ========== AUTH BACKUP HANDLER ==========
document.addEventListener('click', function(ev) {
  var t = ev.target.closest('button, a');
  if (!t) return;
  var txt = (t.textContent || '').trim().toLowerCase();
  if (txt.indexOf('register org') !== -1) {
    ev.preventDefault();
    try { if (typeof switchAuth === 'function') switchAuth('register'); } catch(e){}
  }
  if (txt.indexOf('quick demo login') !== -1 || txt.indexOf('demo login') !== -1) {
    ev.preventDefault();
    try { if (typeof quickDemoLogin === 'function') quickDemoLogin(); } catch(e){}
  }
});
// ==========================================
'''
if 'AUTH BACKUP HANDLER' not in content:
    content = content.replace("window.addEventListener('DOMContentLoaded'", backup + "\nwindow.addEventListener('DOMContentLoaded'", 1)
    changes.append('Backup handler added')

with open(html_path, 'w') as f:
    f.write(content)

print("=" * 45)
print("✅ Hojii xumurameera!")
for c in changes:
    print("  • " + c)
if not changes:
    print("  ⚠️ Wanti jijjiirame hin jiru.")
print("=" * 45)

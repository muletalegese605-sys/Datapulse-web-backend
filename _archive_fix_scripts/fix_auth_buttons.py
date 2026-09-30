import os, re

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    content = f.read()

# 1. Mirkaneessi: switchAuth function jiraachuu fi dhabuu
if 'function switchAuth' in content:
    print("✅ Function 'switchAuth' ni jira.")
else:
    print("⚠️ Function 'switchAuth' hin jiru. Function haaraa dabalna.")

# 2. Global event listener (backup) dabaluu
backup_listener = '''
// ========== AUTH BUTTONS BACKUP HANDLER ==========
document.addEventListener('click', function(ev) {
  var btn = ev.target.closest('button');
  if (!btn) return;
  var txt = (btn.textContent || '').trim().toLowerCase();
  
  // Register Org button
  if (txt.indexOf('register org') !== -1) {
    ev.preventDefault();
    ev.stopPropagation();
    try {
      if (typeof switchAuth === 'function') { switchAuth('register'); return; }
      var regTab = document.getElementById('tbRegister');
      if (regTab) { regTab.click(); return; }
      var forms = document.querySelectorAll('[id*="register"], [id*="Register"]');
      forms.forEach(function(f){ if (f.id) { f.classList.remove('hidden'); f.style.display = ''; } });
      var loginForms = document.querySelectorAll('[id*="login"], [id*="Login"]');
      loginForms.forEach(function(f){ if (f.id && f.id !== 'loginScreen') { f.classList.add('hidden'); f.style.display = 'none'; } });
      if (typeof toast === 'function') toast('Register form opened', 'info');
    } catch(e) { console.warn('Register button failed:', e.message); }
  }
  
  // Quick Demo Login button
  if (txt.indexOf('quick demo login') !== -1 || txt.indexOf('demo login') !== -1) {
    ev.preventDefault();
    ev.stopPropagation();
    try {
      if (typeof quickDemoLogin === 'function') { quickDemoLogin(); return; }
      if (typeof demoLogin === 'function') { demoLogin(); return; }
      var em = document.getElementById('loginEmail') || document.querySelector('input[type=email]');
      var pw = document.getElementById('loginPass') || document.querySelector('input[type=password]');
      if (em) em.value = 'demo@datapulse.com';
      if (pw) pw.value = 'demo1234';
      var loginBtn = document.getElementById('btnLogin') || document.getElementById('loginBtn') || document.querySelector('button[onclick*="login"], button[onclick*="Login"]');
      if (loginBtn) { loginBtn.click(); return; }
      var screen = document.getElementById('loginScreen');
      if (screen) { screen.classList.add('hidden'); }
      var app = document.getElementById('app');
      if (app) { app.classList.remove('hidden'); }
      if (typeof render === 'function') render();
      if (typeof toast === 'function') toast('Demo login successful', 'success');
    } catch(e) { console.warn('Demo button failed:', e.message); }
  }
});
// ==================================================
'''

if 'AUTH BUTTONS BACKUP HANDLER' not in content:
    content = content.replace(
        'window.addEventListener(\'DOMContentLoaded\'',
        backup_listener + '\nwindow.addEventListener(\'DOMContentLoaded\'',
        1
    )
    print("✅ Global auth handler dabalameera!")
else:
    print("⚠️ Auth handler amma jira.")

# 3. Yoo 'switchAuth' hin jiraanne, function dabalii
if 'function switchAuth' not in content:
    fallback_fn = '''
function switchAuth(mode) {
  try {
    var tabs = document.querySelectorAll('[id^="tb"]');
    tabs.forEach(function(t){
      t.classList.remove('bg-emerald-500/20','text-emerald-400','border-emerald-500/50');
      t.classList.add('text-slate-400');
    });
    var target = document.getElementById('tb' + mode.charAt(0).toUpperCase() + mode.slice(1));
    if (target) {
      target.classList.remove('text-slate-400');
      target.classList.add('bg-emerald-500/20','text-emerald-400','border-emerald-500/50');
    }
    document.querySelectorAll('[id*="loginForm"], [id*="LoginForm"]').forEach(function(f){ f.classList.add('hidden'); f.style.display='none'; });
    document.querySelectorAll('[id*="registerForm"], [id*="RegisterForm"]').forEach(function(f){ f.classList.remove('hidden'); f.style.display=''; });
  } catch(e) { console.warn('switchAuth error:', e.message); }
}
'''
    content = content.replace(
        'window.addEventListener(\'DOMContentLoaded\'',
        fallback_fn + '\nwindow.addEventListener(\'DOMContentLoaded\'',
        1
    )
    print("✅ Function 'switchAuth' dabalameera!")

with open(html_path, 'w') as f:
    f.write(content)

print("📍 Hojii xumurameera!")

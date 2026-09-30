import os, re

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    content = f.read()

changes = []

# 1. Sign In tab: inline JS
signin_js = "document.getElementById('loginForm').classList.remove('hidden');document.getElementById('regForm').classList.add('hidden');this.classList.add('bg-emerald-500','text-slate-950');this.classList.remove('text-slate-400');var r=document.getElementById('tbRegister');if(r){r.classList.remove('bg-emerald-500','text-slate-950');r.classList.add('text-slate-400');}"

content = re.sub(
    r'(<button[^>]*id="tbLogin"[^>]*?)\s*onclick="[^"]*"',
    r'\1 onclick="' + signin_js + '"',
    content
)
if 'id="tbLogin"' in content:
    changes.append('Sign In tab: inline JS')

# 2. Register Org tab: inline JS
register_js = "document.getElementById('regForm').classList.remove('hidden');document.getElementById('loginForm').classList.add('hidden');this.classList.add('bg-emerald-500','text-slate-950');this.classList.remove('text-slate-400');var l=document.getElementById('tbLogin');if(l){l.classList.remove('bg-emerald-500','text-slate-950');l.classList.add('text-slate-400');}"

content = re.sub(
    r'(<button[^>]*id="tbRegister"[^>]*?)\s*onclick="[^"]*"',
    r'\1 onclick="' + register_js + '"',
    content
)
if 'id="tbRegister"' in content:
    changes.append('Register Org tab: inline JS')

# 3. Log In button: inline JS (form submit)
content = re.sub(
    r'(<button[^>]*type="submit"[^>]*>[\s\S]{0,200}?Log In)',
    lambda m: m.group(0) if 'onclick' in m.group(0) else m.group(0).replace('<button', '<button onclick="document.getElementById(\'loginForm\').requestSubmit()"', 1),
    content
)

# 4. Quick Demo Login: inline JS
demo_js = "localStorage.setItem('dp_demo_user',JSON.stringify({name:'Demo Admin',email:'demo@datapulse.com',role:'admin'}));var ls=document.getElementById('loginScreen');if(ls)ls.classList.add('hidden');var app=document.getElementById('app');if(app){app.classList.remove('hidden');app.style.display='';}if(typeof state!=='undefined'){state.user={name:'Demo Admin',email:'demo@datapulse.com',role:'admin'};state.org={id:'ORG-DEMO',name:'Demo Enterprise'};}if(typeof render==='function')render();if(typeof toast==='function')toast('Demo login successful','success');"

content = re.sub(
    r'(<button[^>]*?)\s*onclick="[^"]*quickDemo[^"]*"([^>]*>[\s\S]{0,150}?Quick Demo Login)',
    r'\1 onclick="' + demo_js + r'"\2',
    content
)
if 'Quick Demo Login' in content:
    changes.append('Quick Demo Login: inline JS')

# 5. Backup handler: onclick attr haqii, event delegation (DOM-level)
# Kun button-wwan onclick attribute hin qabanillee ni hojjeta
backup = '''
// ========== UNIVERSAL BUTTON HANDLER ==========
document.addEventListener('click', function(ev) {
  var t = ev.target.closest('button, a');
  if (!t) return;
  var txt = (t.textContent || '').trim().toLowerCase();
  var id = t.id || '';
  
  // Sign In tab
  if (id === 'tbLogin' || (txt === 'sign in' && t.tagName === 'BUTTON')) {
    ev.preventDefault();
    try {
      var lf = document.getElementById('loginForm');
      var rf = document.getElementById('regForm');
      if (lf) lf.classList.remove('hidden');
      if (rf) rf.classList.add('hidden');
      if (t.id) t.className = t.className.replace(/text-slate-400/g, 'text-slate-950').replace(/hover:text-emerald-400/g, '') + ' bg-emerald-500';
      var rb = document.getElementById('tbRegister');
      if (rb) rb.className = rb.className.replace(/bg-emerald-500/g, '').replace(/text-slate-950/g, 'text-slate-400');
    } catch(e) { console.warn('Sign In tab error:', e); }
    return;
  }
  
  // Register Org tab
  if (id === 'tbRegister' || txt.indexOf('register org') !== -1) {
    ev.preventDefault();
    try {
      var lf = document.getElementById('loginForm');
      var rf = document.getElementById('regForm');
      if (lf) lf.classList.add('hidden');
      if (rf) rf.classList.remove('hidden');
      if (t.id) t.className = t.className.replace(/text-slate-400/g, 'text-slate-950').replace(/hover:text-emerald-400/g, '') + ' bg-emerald-500';
      var lb = document.getElementById('tbLogin');
      if (lb) lb.className = lb.className.replace(/bg-emerald-500/g, '').replace(/text-slate-950/g, 'text-slate-400');
    } catch(e) { console.warn('Register tab error:', e); }
    return;
  }
  
  // Quick Demo Login
  if (txt.indexOf('quick demo login') !== -1) {
    ev.preventDefault();
    try {
      localStorage.setItem('dp_demo_user', JSON.stringify({name:'Demo Admin', email:'demo@datapulse.com', role:'admin'}));
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
    } catch(e) { console.warn('Demo error:', e); }
    return;
  }
  
  // Log In button
  if (txt.indexOf('log in') !== -1 && t.tagName === 'BUTTON') {
    var lf2 = document.getElementById('loginForm');
    if (lf2 && typeof lf2.requestSubmit === 'function') {
      ev.preventDefault();
      lf2.requestSubmit();
    }
    return;
  }
});
// ==========================================
'''
if 'UNIVERSAL BUTTON HANDLER' not in content:
    if '// ========== AUTH BACKUP HANDLER ==========' in content:
        # Handler duraa haqii, kan haaraa galchi
        content = re.sub(
            r'// ========== AUTH BACKUP HANDLER ==========.*?// ==========================================',
            backup,
            content, count=1, flags=re.DOTALL
        )
    else:
        content = content.replace("window.addEventListener('DOMContentLoaded'", backup + "\nwindow.addEventListener('DOMContentLoaded'", 1)
    changes.append('Universal button handler dabalameera')

with open(html_path, 'w') as f:
    f.write(content)

print("=" * 50)
print("✅ Hojii xumurameera!")
for c in changes:
    print("  • " + c)
if not changes:
    print("  ⚠️ Wanti jijjiirame hin jiru.")
print("=" * 50)

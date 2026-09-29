import os, re

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    content = f.read()

print("=" * 60)
print("🔧 SHOWLOGINFROMLANDING - ROBUST FIX")
print("=" * 60)

# 1. Dura function ammaa fi maal akka qabu ilaali
m = re.search(r'function\s+showLoginFromLanding\s*\(\s*\)\s*\{', content)
if m:
    start = m.start()
    depth = 0
    end = start
    for i in range(m.end() - 1, len(content)):
        if content[i] == '{': depth += 1
        elif content[i] == '}':
            depth -= 1
            if depth == 0:
                end = i + 1
                break
    old_fn = content[start:end]
    line_no = content[:start].count('\n') + 1
    print(f"\n1. Function duraa (Sarara {line_no}):")
    print(f"   {old_fn[:300]}")
else:
    print("\n1. ⚠️ Function hin argamne!")

# 2. Function haaraa - nageenya qabu, fallback waliin
new_fn = '''function showLoginFromLanding(){
  try {
    // Landing page dhoksi (yoo jiraate)
    var lp = document.getElementById('landingPage');
    if (lp) {
      lp.classList.add('hidden');
      lp.style.display = 'none';
    } else {
      console.warn('showLoginFromLanding: #landingPage hin argamne');
    }
    
    // Login screen bani (yoo jiraate)
    var ls = document.getElementById('loginScreen');
    if (ls) {
      ls.classList.remove('hidden');
      ls.style.display = '';
      ls.removeAttribute('hidden');
      ls.classList.add('flex');
      console.log('✅ Login screen banameera');
    } else {
      // Fallback: login screen dhabame, dashboard geessi
      console.warn('showLoginFromLanding: #loginScreen hin argamne, dashboard geessa');
      var app = document.getElementById('app');
      if (app) {
        app.classList.remove('hidden');
        app.style.display = '';
        app.removeAttribute('hidden');
      }
      var main = document.getElementById('main');
      if (main) {
        main.classList.remove('hidden');
        main.style.display = '';
        main.removeAttribute('hidden');
      }
      if (typeof state !== 'undefined') {
        if (!state.tab) state.tab = 'dashboard';
        if (!state.org) state.org = {id: 'ORG-DEMO', name: 'Demo Enterprise'};
        if (!Array.isArray(state.records)) state.records = [];
      }
      if (typeof render === 'function') {
        try { render(); } catch(e) { console.warn('render err:', e.message); }
      }
    }
  } catch(e) {
    console.error('showLoginFromLanding RAKKOO:', e.message);
    // Fallback dhumaa: app mul'achiisi
    try {
      var app2 = document.getElementById('app');
      if (app2) { app2.classList.remove('hidden'); app2.style.display = ''; }
      var main2 = document.getElementById('main');
      if (main2) { main2.classList.remove('hidden'); main2.style.display = ''; }
    } catch(e2) {}
  }
}'''

# 3. Function duraa bakka buusi
if m:
    content = content[:start] + new_fn + content[end:]
    print("\n✅ Function guutummaatti bakka bu'ameera!")
else:
    # Yoo hin jiraanne, script tag keessatti dabali
    last_close = content.rfind('</script>')
    if last_close > 0:
        content = content[:last_close] + '\n' + new_fn + '\n' + content[last_close:]
        print("\n✅ Function haaraa dabalameera (</script> dura)")
    else:
        print("\n❌ Script tag hin argamne!")

# 4. Backup button handler - Launch App hunda
backup = '''
// ========== SHOWLOGIN BACKUP HANDLER ==========
document.addEventListener('click', function(ev) {
  var t = ev.target.closest('button, a');
  if (!t) return;
  var txt = (t.textContent || '').trim().toLowerCase();
  
  // Launch App, Start Free Trial, See Features
  if (txt.indexOf('launch app') !== -1 || txt.indexOf('start free trial') !== -1 || txt.indexOf('see features') !== -1) {
    ev.preventDefault();
    console.log('Backup handler: ' + txt + ' tuqame');
    try {
      var lp = document.getElementById('landingPage'); if (lp) { lp.classList.add('hidden'); lp.style.display = 'none'; }
      var ls = document.getElementById('loginScreen');
      if (ls) {
        ls.classList.remove('hidden');
        ls.style.display = '';
        ls.classList.add('flex');
      } else {
        var app = document.getElementById('app'); if (app) { app.classList.remove('hidden'); app.style.display = ''; }
        var main = document.getElementById('main'); if (main) { main.classList.remove('hidden'); main.style.display = ''; }
        if (typeof state !== 'undefined') { state.tab = state.tab || 'dashboard'; }
        if (typeof render === 'function') { try { render(); } catch(e) {} }
      }
    } catch(e) { console.warn('backup err:', e.message); }
    return;
  }
}, true);
// ==============================================
'''

if 'SHOWLOGIN BACKUP HANDLER' not in content:
    last_close = content.rfind('</script>')
    if last_close > 0:
        content = content[:last_close] + backup + '\n' + content[last_close:]
        print("✅ Backup handler dabalameera")

# Save
with open(html_path, 'w') as f:
    f.write(content)

# 5. Mirkaneessi
with open(html_path, 'r') as f:
    new_content = f.read()

print("\n" + "=" * 60)
print("📍 MIRKANEESSA")
print("=" * 60)

# Function haaraa check
if 'function showLoginFromLanding' in new_content:
    idx = new_content.find('function showLoginFromLanding')
    line_no = new_content[:idx].count('\n') + 1
    print(f"   ✅ showLoginFromLanding (Sarara {line_no})")
    
    # Try/catch jira?
    fn_part = new_content[idx:idx+2000]
    has_try = 'try {' in fn_part
    has_lp = 'landingPage' in fn_part
    has_ls = 'loginScreen' in fn_part
    has_fallback = 'app' in fn_part
    print(f"   try/catch: {'✅' if has_try else '❌'}")
    print(f"   landingPage check: {'✅' if has_lp else '❌'}")
    print(f"   loginScreen check: {'✅' if has_ls else '❌'}")
    print(f"   Fallback (app): {'✅' if has_fallback else '❌'}")

# Script balance
opens = len(re.findall(r'<script\b[^>]*>', new_content))
closes = new_content.count('</script>')
print(f"\n   Script balance: {opens} / {closes}")

print("\n" + "=" * 60)
print("✅ XUMURAMEERA!")
print("=" * 60)

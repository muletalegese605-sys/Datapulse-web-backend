import os, re

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    content = f.read()

print("=" * 60)
print("🔧 QUICKDEMOLOGIN FUNCTION FIX")
print("=" * 60)

# 1. Dura mirkaneessi - jira moo hin jiru?
existing = re.findall(r'function\s+quickDemoLogin\s*\(', content)
print(f"\n1. quickDemoLogin hunda: {len(existing)}")

if len(existing) > 0:
    print("   ✅ Function sun duraan jira. Bakka isaa ilaali:")
    for m in re.finditer(r'function\s+quickDemoLogin\s*\(', content):
        line_no = content[:m.start()].count('\n') + 1
        print(f"      Sarara {line_no}")
        # Script keessa jira?
        before = content[:m.start()]
        last_open = before.rfind('<script')
        last_close = before.rfind('</script>')
        in_script = last_open > last_close
        print(f"      Script keessa: {'✅' if in_script else '❌ SCRIPT ALAAAA'}")
else:
    print("   ⚠️  Function hin jiru. Amma dabaluu qabna.")

# 2. Function haaraa qopheessi
demo_fn = '''
// ========== QUICK DEMO LOGIN ==========
function quickDemoLogin() {
  try {
    // Demo user localStorage keessatti galmeessi
    localStorage.setItem('dp_demo_user', JSON.stringify({
      name: 'Demo Admin',
      email: 'demo@datapulse.com',
      role: 'admin'
    }));
    
    // Landing fi login screens dhoksi
    var lp = document.getElementById('landingPage');
    if (lp) lp.classList.add('hidden');
    var ls = document.getElementById('loginScreen');
    if (ls) ls.classList.add('hidden');
    
    // App fi main mul'achiisi
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
    
    // State mirkaneessi
    if (typeof state !== 'undefined') {
      state.user = {name: 'Demo Admin', email: 'demo@datapulse.com', role: 'admin'};
      state.org = {id: 'ORG-DEMO', name: 'Demo Enterprise'};
      if (!state.tab) state.tab = 'dashboard';
      if (!Array.isArray(state.records)) state.records = [];
    }
    
    // Render fi data fidu
    if (typeof render === 'function') render();
    if (typeof DP !== 'undefined' && DP.api && DP.api.loadAll) {
      DP.api.loadAll();
    }
    if (typeof toast === 'function') toast('Demo login successful', 'success');
    
    console.log('✅ Quick Demo Login hoijeteera!');
  } catch(e) {
    console.error('quickDemoLogin error:', e.message);
    alert('Demo login error: ' + e.message);
  }
}
// =====================================
'''

# 3. Function dabaluu - script tag keessatti
if len(existing) == 0:
    # Bakka window.addEventListener('DOMContentLoaded') dura galchi
    # Kun script tag guddaa keessatti jiraachuu qaba
    target = "window.addEventListener('DOMContentLoaded'"
    if target in content:
        # Kun script keessa jira - mirkaneessi
        idx = content.find(target)
        before = content[:idx]
        last_open = before.rfind('<script')
        last_close = before.rfind('</script>')
        in_script = last_open > last_close
        
        if in_script:
            content = content[:idx] + demo_fn + '\n' + content[idx:]
            print("\n   ✅ Function sun script tag keessatti dabalameera")
        else:
            # Yoo script ala ta'e, script tag haaraa uumi
            content = content.replace(target, demo_fn + '\n<script>\n' + target, 1)
            content = content.replace('window.addEventListener(\'DOMContentLoaded\', () => {', '</script>\nwindow.addEventListener(\'DOMContentLoaded\', () => {', 1)
            print("\n   ✅ Function sun script tag haaraa keessatti dabalameera")
    else:
        # Fallback: </script> dura galchi
        last_close = content.rfind('</script>')
        if last_close > 0:
            content = content[:last_close] + demo_fn + '\n' + content[last_close:]
            print("\n   ✅ Function sun </script> dura dabalameera")
        else:
            print("\n   ❌ Script tag hin argamne!")

with open(html_path, 'w') as f:
    f.write(content)

# 4. Mirkaneessi
with open(html_path, 'r') as f:
    new_content = f.read()

print("\n" + "=" * 60)
print("📍 MIRKANEESSA")
print("=" * 60)

new_count = len(re.findall(r'function\s+quickDemoLogin\s*\(', new_content))
print(f"   quickDemoLogin function: {new_count}")

if new_count > 0:
    for m in re.finditer(r'function\s+quickDemoLogin\s*\(', new_content):
        line_no = new_content[:m.start()].count('\n') + 1
        before = new_content[:m.start()]
        last_open = before.rfind('<script')
        last_close = before.rfind('</script>')
        in_script = last_open > last_close
        print(f"   Sarara {line_no}: Script keessa = {'✅ EEYY' if in_script else '❌ LAKKI'}")

# Script tags balance
opens = len(re.findall(r'<script\b[^>]*>', new_content))
closes = new_content.count('</script>')
print(f"\n   <script>: {opens}, </script>: {closes}, Diff: {opens - closes}")

# quickDemoLogin calls
calls = len(re.findall(r'quickDemoLogin\s*\(\s*\)', new_content))
print(f"\n   quickDemoLogin() calls: {calls}")

print("\n" + "=" * 60)
print("✅ XUMURAMEERA!")
print("=" * 60)

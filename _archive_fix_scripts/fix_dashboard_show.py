import os, re

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    content = f.read()

changes = []

# 1. Universal login/demo handler: dashboard fi app lamaanuu mul'achuu qabu
universal_fix = '''
// ========== DASHBOARD SHOW FIX ==========
function forceShowDashboard() {
  try {
    ['dashboard', 'app'].forEach(function(id) {
      var el = document.getElementById(id);
      if (el) {
        el.classList.remove('hidden');
        el.style.display = '';
        el.removeAttribute('hidden');
      }
    });
    var ls = document.getElementById('loginScreen');
    if (ls) ls.classList.add('hidden');
    var lp = document.getElementById('landingPage');
    if (lp) lp.classList.add('hidden');
    if (typeof render === 'function') render();
    if (typeof DP !== 'undefined' && DP.api && DP.api.loadAll) DP.api.loadAll();
  } catch(e) { console.warn('forceShowDashboard error:', e.message); }
}

document.addEventListener('click', function(ev) {
  var t = ev.target.closest('button, a');
  if (!t) return;
  var txt = (t.textContent || '').trim().toLowerCase();
  if (txt.indexOf('quick demo login') !== -1 || txt === 'log in' || txt === 'sign in') {
    setTimeout(forceShowDashboard, 300);
  }
}, true);

window.addEventListener('load', function() {
  setTimeout(function() {
    var d = document.getElementById('dashboard');
    var a = document.getElementById('app');
    if (d && !d.classList.contains('hidden')) forceShowDashboard();
    if (a && !a.classList.contains('hidden')) forceShowDashboard();
  }, 500);
});
// ========================================
'''

if 'DASHBOARD SHOW FIX' not in content:
    content = content.replace(
        "window.addEventListener('DOMContentLoaded'",
        universal_fix + "\nwindow.addEventListener('DOMContentLoaded'",
        1
    )
    changes.append('forceShowDashboard function dabalameera')

# 2. doLogin function keessatti dashboard mul'achuu mirkaneessi
if 'function doLogin' in content:
    # Yoo doLogin keessatti 'dashboard' hidden haqaa jiraachuu baate, dabaluu
    if "getElementById('dashboard').classList.remove('hidden')" not in content:
        pattern = re.compile(r'(function\s+doLogin\s*\([^)]*\)\s*\{)')
        content = pattern.sub(
            r"\1\n  forceShowDashboard();\n",
            content, count=1
        )
        changes.append('doLogin: forceShowDashboard() dabalameera')

# 3. render() function sun dashboard data akka guutu mirkaneessi
# Yoo render() keessatti state.records fayyadamee, data duwwaa ta'ee, "0" agarsiisa.
# Kanaaf DP.api.loadAll() booda render() deebi'ee akka hojjetu godhi
if 'function render()' in content:
    old_render_start = content.find('function render()')
    if old_render_start != -1:
        # DP.api.loadAll() render keessatti dabaluu
        if 'DP.api.loadAll' not in content[old_render_start:old_render_start+1000]:
            content = content[:old_render_start + len('function render() {')] + "\n  try { if (typeof DP !== 'undefined' && DP.api && DP.api.loadAll && !window._dpLoading) { window._dpLoading = true; DP.api.loadAll().finally(function(){ window._dpLoading = false; }); } } catch(e) {}\n" + content[old_render_start + len('function render() {'):]
            changes.append('render(): DP.api.loadAll() dabalameera')

with open(html_path, 'w') as f:
    f.write(content)

print("=" * 50)
print("✅ Hojii xumurameera!")
for c in changes:
    print("  • " + c)
if not changes:
    print("  ⚠️ Wanti jijjiirame hin jiru.")
print("=" * 50)

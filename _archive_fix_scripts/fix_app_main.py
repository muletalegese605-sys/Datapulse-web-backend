import os, re

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    content = f.read()

# 1. #app element irraa 'hidden' haqi
content = re.sub(
    r'(<div[^>]*id="app"[^>]*class=")[^"]*"',
    r'\1min-h-screen pb-20 md:pb-0"',
    content
)
print("✅ #app irraa 'hidden' haqameera!")

# 2. #main element irraa 'hidden' haqi (yoo jiraate)
content = re.sub(
    r'(<main[^>]*id="main"[^>]*class=")[^"]*"',
    r'\1max-w-7xl mx-auto px-3 sm:px-4 py-4 sm:py-6"',
    content
)
print("✅ #main irraa 'hidden' haqameera!")

# 3. #landingPage fi #loginScreen haqi (hidden dhiisi)
# Kun rakkoo miti, isaan sun hidden ta'uu qabu

# 4. render() sun yeroo hunda hojjechuu mirkaneessi
nuclear2 = '''
// ========== FINAL DASHBOARD RENDER ==========
(function() {
  function forceRender() {
    try {
      var main = document.getElementById('main');
      var app = document.getElementById('app');
      
      if (!main) return;
      
      // #app irraa hidden haqi
      if (app) { app.classList.remove('hidden'); app.style.display = ''; app.removeAttribute('hidden'); }
      main.classList.remove('hidden'); main.style.display = ''; main.removeAttribute('hidden');
      
      // State mirkaneessi
      if (typeof state !== 'undefined') {
        if (!state.tab) state.tab = 'dashboard';
        if (!state.org) state.org = {id: 'ORG-DEMO', name: 'Demo Enterprise'};
        if (!state.user) state.user = {name: 'Demo Admin', email: 'demo@datapulse.com', role: 'admin'};
        if (!Array.isArray(state.records)) state.records = [];
      }
      
      // Render hojjedhu
      if (typeof render === 'function') {
        try { render(); } catch(e) {
          main.innerHTML = '<div style="padding:20px;color:#ef4444;font-family:monospace;font-size:12px;"><b>Render Error:</b><br>' + e.message + '</div>';
        }
      }
      
      // Yoo ammas duwwaa ta'e, diagnostic info
      if (main.innerHTML.trim().length < 100) {
        var recCount = (typeof state !== 'undefined' && state.records) ? state.records.length : 'NO_STATE';
        main.innerHTML = '<div style="padding:20px;font-family:monospace;font-size:12px;color:#10b981;">' +
          '<b>Diagnostic:</b><br>' +
          'state.records: ' + recCount + '<br>' +
          'render() exists: ' + (typeof render === 'function') + '<br>' +
          'vDash() exists: ' + (typeof vDash === 'function') + '<br>' +
          'state.tab: ' + ((typeof state !== 'undefined' && state.tab) || 'N/A') + '<br>' +
          '</div>';
      }
    } catch(e) { console.warn('forceRender error:', e.message); }
  }
  
  // Yeroo app banamu
  window.addEventListener('load', function() {
    setTimeout(forceRender, 500);
    setTimeout(forceRender, 1500);
    setTimeout(forceRender, 3000);
  });
  
  // Yeroo login/demo tuqtu
  document.addEventListener('click', function(ev) {
    var t = ev.target.closest('button, a');
    if (!t) return;
    var txt = (t.textContent || '').trim().toLowerCase();
    if (txt.indexOf('quick demo login') !== -1 || txt === 'log in' || txt === 'sign in') {
      setTimeout(forceRender, 800);
      setTimeout(forceRender, 2000);
    }
  }, true);
  
  // Yeroo hunda, yoo main duwwaa ta'e, render
  setInterval(function() {
    try {
      var main = document.getElementById('main');
      if (main && main.innerHTML.trim().length < 100) {
        var app = document.getElementById('app');
        if (app && !app.classList.contains('hidden')) forceRender();
      }
    } catch(e) {}
  }, 2000);
})();
// =============================================
'''

if 'FINAL DASHBOARD RENDER' not in content:
    content = content.replace('</body>', nuclear2 + '\n</body>')
    print("✅ FINAL DASHBOARD RENDER dabalameera!")

with open(html_path, 'w') as f:
    f.write(content)

print("📍 Hojii xumurameera!")

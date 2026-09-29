import os

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    content = f.read()

nuclear = '''
// ========== NUCLEAR DASHBOARD FIX ==========
(function() {
  var attempts = 0;
  var timer = setInterval(function() {
    attempts++;
    if (attempts > 60) { clearInterval(timer); return; }
    
    try {
      var main = document.getElementById('main');
      var app = document.getElementById('app');
      var ls = document.getElementById('loginScreen');
      var lp = document.getElementById('landingPage');
      
      if (!main || !app) return;
      
      // Yoo landing fi login hidden ta'aniif, app mul'achuu qaba
      var lsHidden = !ls || ls.classList.contains('hidden') || ls.style.display === 'none';
      var lpHidden = !lp || lp.classList.contains('hidden') || lp.style.display === 'none';
      
      if (lsHidden && lpHidden) {
        app.classList.remove('hidden');
        app.style.display = '';
        app.removeAttribute('hidden');
        main.classList.remove('hidden');
        main.style.display = '';
        main.removeAttribute('hidden');
        
        // Yoo main duwwaa ta'e, render yaali
        if (main.innerHTML.trim().length < 100) {
          if (typeof state !== 'undefined') {
            if (!state.tab) state.tab = 'dashboard';
            if (!state.org) state.org = {id: 'ORG-DEMO', name: 'Demo Enterprise'};
            if (!Array.isArray(state.records)) state.records = [];
          }
          
          if (typeof render === 'function') {
            try { render(); } catch(e) {
              main.innerHTML = '<div style="padding:20px;color:#ef4444;font-family:monospace;font-size:12px;"><b>Render Error:</b><br>' + e.message + '</div>';
            }
          }
          
          // Yoo ammas duwwaa ta'e, debug info agarsiisi
          if (main.innerHTML.trim().length < 100) {
            var recCount = (typeof state !== 'undefined' && state.records) ? state.records.length : 'NO_STATE';
            main.innerHTML = '<div style="padding:20px;font-family:monospace;font-size:12px;color:#10b981;">' +
              '<b>Diagnostic Info:</b><br>' +
              'state.records: ' + recCount + '<br>' +
              'render() exists: ' + (typeof render === 'function') + '<br>' +
              'vDash() exists: ' + (typeof vDash === 'function') + '<br>' +
              'kpis() exists: ' + (typeof kpis === 'function') + '<br>' +
              'state.tab: ' + ((typeof state !== 'undefined' && state.tab) || 'N/A') + '<br>' +
              '</div>';
          }
        }
        
        // Yoo guutuu ta'e, monitor dhaabi
        if (main.innerHTML.trim().length > 300) clearInterval(timer);
      }
    } catch(e) { /* silent */ }
  }, 800);
})();
// =============================================
'''

if 'NUCLEAR DASHBOARD FIX' not in content:
    content = content.replace('</body>', nuclear + '\n</body>')
    print("✅ NUCLEAR FIX dabalameera!")

with open(html_path, 'w') as f:
    f.write(content)

print("📍 Hojii xumurameera!")

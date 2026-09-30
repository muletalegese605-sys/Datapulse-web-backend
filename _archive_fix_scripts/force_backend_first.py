import os, re

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    content = f.read()

# Yoo init sun jiraate, ofumaan backend irraa data fidi
init_fix = '''
// ========== BACKEND FIRST LOADER ==========
(function() {
  function bootstrap() {
    try {
      // Yeroo app banamu, backend irraa data fidu - localStorage dura
      if (window.DP && DP.api && DP.api.loadAll) {
        var origLoadAll = DP.api.loadAll.bind(DP.api);
        DP.api.loadAll = async function() {
          try { await origLoadAll(); } catch(e) {}
          try {
            // Data backend irraa dhufe - localStorage irrattis galmeessi
            if (DP.api._cache && DP.api._cache.records && DP.api._cache.records.length) {
              state.records = DP.api._cache.records;
              if (typeof saveRecords === 'function') saveRecords();
            }
          } catch(e) {}
          try { if (typeof render === 'function') render(); } catch(e) {}
        };
        // Ofumaan yeroo app banamu fidu
        DP.api.loadAll();
      }
    } catch(e) { console.warn('Bootstrap error:', e.message); }
  }
  
  // Yeroo DOM qophaa'e, bootstrap hojjedhu
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function(){ setTimeout(bootstrap, 500); });
  } else {
    setTimeout(bootstrap, 500);
  }
  
  // Yeroo login/demo tuqtu, ammas data fidu
  document.addEventListener('click', function(ev) {
    var t = ev.target.closest('button, a');
    if (!t) return;
    var txt = (t.textContent || '').trim().toLowerCase();
    if (txt.indexOf('quick demo login') !== -1 || txt === 'log in') {
      setTimeout(function() {
        if (window.DP && DP.api && DP.api.loadAll) DP.api.loadAll();
      }, 800);
    }
  }, true);
})();
// ===========================================
'''

if 'BACKEND FIRST LOADER' not in content:
    content = content.replace(
        "window.addEventListener('DOMContentLoaded'",
        init_fix + "\nwindow.addEventListener('DOMContentLoaded'",
        1
    )
    with open(html_path, 'w') as f:
        f.write(content)
    print("✅ Backend-first loader dabalameera!")
else:
    print("⚠️  Loader amma jira.")


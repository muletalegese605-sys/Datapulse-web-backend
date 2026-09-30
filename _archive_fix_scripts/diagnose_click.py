import os, re

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    content = f.read()

# Diagnostic overlay - button tuqame hunda ni agarsiisa
diag = '''
<script>
// ========== CLICK DIAGNOSTIC ==========
(function() {
  function showMsg(msg) {
    var d = document.getElementById('diagMsg');
    if (!d) {
      d = document.createElement('div');
      d.id = 'diagMsg';
      d.style.cssText = 'position:fixed;bottom:100px;left:10px;right:10px;z-index:99999;background:#1e293b;border:2px solid #10b981;border-radius:8px;padding:10px;font-family:monospace;font-size:11px;color:#e2e8f0;max-height:40vh;overflow:auto;';
      document.body.appendChild(d);
    }
    var time = new Date().toLocaleTimeString();
    d.innerHTML = '<div style="color:#10b981;font-weight:bold;">' + time + '</div>' + msg;
  }
  
  document.addEventListener('click', function(ev) {
    var t = ev.target.closest('button, a');
    if (!t) return;
    var txt = (t.textContent || '').trim().substring(0, 30);
    var onclick = t.getAttribute('onclick') || 'NO_ONCLICK';
    var id = t.id || 'NO_ID';
    
    // Try to execute the function manually
    var result = 'NO_FUNCTION';
    if (onclick.indexOf('showLoginFromLanding') !== -1) {
      try {
        if (typeof showLoginFromLanding === 'function') {
          showLoginFromLanding();
          result = 'CALLED_OK';
        } else {
          result = 'FUNCTION_NOT_FOUND';
        }
      } catch(e) {
        result = 'ERROR: ' + e.message;
      }
    }
    
    // Check element states after
    var lp = document.getElementById('landingPage');
    var ls = document.getElementById('loginScreen');
    var app = document.getElementById('app');
    
    showMsg(
      '<b>Button:</b> "' + txt + '"<br>' +
      '<b>ID:</b> ' + id + '<br>' +
      '<b>onclick:</b> ' + onclick.substring(0, 60) + '<br>' +
      '<b>Result:</b> ' + result + '<br>' +
      '<hr style="border-color:#334155;margin:4px 0">' +
      'landingPage hidden: ' + (lp ? lp.classList.contains('hidden') : 'NULL') + '<br>' +
      'loginScreen hidden: ' + (ls ? ls.classList.contains('hidden') : 'NULL') + '<br>' +
      'app hidden: ' + (app ? app.classList.contains('hidden') : 'NULL') + '<br>' +
      'showLoginFromLanding: ' + (typeof showLoginFromLanding) + '<br>' +
      'render: ' + (typeof render) + '<br>' +
      'state: ' + (typeof state)
    );
  }, true);
})();
</script>
'''

if 'CLICK DIAGNOSTIC' not in content:
    content = content.replace('</body>', diag + '\n</body>')
    with open(html_path, 'w') as f:
        f.write(content)
    print("✅ Click diagnostic dabalameera!")
else:
    print("⚠️  Diagnostic amma jira.")

print("📍 Hojii xumurameera!")

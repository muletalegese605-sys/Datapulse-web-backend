import os, re

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    content = f.read()

# Diagnostic script - visible, auto-run
diag = '''
<script>
// ========== VISIBLE DIAGNOSTIC OVERLAY ==========
(function() {
  function showDiag() {
    try {
      var main = document.getElementById('main');
      var app = document.getElementById('app');
      var ls = document.getElementById('loginScreen');
      var lp = document.getElementById('landingPage');
      
      // Yoo main duwwaa ta'e, diagnostic overlay agarsiisi
      if (!main) { alert('ERROR: #main element hin jiru!'); return; }
      
      var mainEmpty = main.innerHTML.trim().length < 50;
      var appHidden = !app || app.classList.contains('hidden');
      var lsHidden = !ls || ls.classList.contains('hidden');
      var lpHidden = !lp || lp.classList.contains('hidden');
      
      // Yoo main duwwaa ta'e, visible diagnostic agarsiisi
      if (mainEmpty || appHidden) {
        var diag = document.createElement('div');
        diag.id = 'diagOverlay';
        diag.style.cssText = 'position:fixed;top:60px;left:10px;right:10px;z-index:99999;background:#0f172a;border:2px solid #10b981;border-radius:12px;padding:16px;font-family:monospace;font-size:11px;color:#e2e8f0;max-height:80vh;overflow:auto;';
        
        var recCount = 'N/A';
        try { recCount = (typeof state !== 'undefined' && state.records) ? state.records.length : 'NO_STATE'; } catch(e) {}
        
        diag.innerHTML = '<div style="color:#10b981;font-weight:bold;margin-bottom:8px;">🔍 DIAGNOSTIC REPORT</div>' +
          '<div>#main content: <b style="color:' + (mainEmpty ? '#ef4444' : '#10b981') + '">' + (mainEmpty ? 'EMPTY' : 'HAS CONTENT (' + main.innerHTML.length + ' chars)') + '</b></div>' +
          '<div>#app hidden: <b style="color:' + (appHidden ? '#ef4444' : '#10b981') + '">' + appHidden + '</b></div>' +
          '<div>#loginScreen hidden: <b>' + lsHidden + '</b></div>' +
          '<div>#landingPage hidden: <b>' + lpHidden + '</b></div>' +
          '<div>state.records: <b>' + recCount + '</b></div>' +
          '<div>state.tab: <b>' + ((typeof state !== 'undefined' && state.tab) || 'N/A') + '</b></div>' +
          '<div>render() exists: <b>' + (typeof render === 'function') + '</b></div>' +
          '<div>vDash() exists: <b>' + (typeof vDash === 'function') + '</b></div>' +
          '<div>kpis() exists: <b>' + (typeof kpis === 'function') + '</b></div>' +
          '<div>DP.api.loadAll: <b>' + (typeof DP !== 'undefined' && DP.api && DP.api.loadAll ? 'YES' : 'NO') + '</b></div>' +
          '<div style="margin-top:8px;padding-top:8px;border-top:1px solid #334155;">' +
          '<button onclick="try{render()}catch(e){alert(e.message)}" style="background:#10b981;color:#fff;padding:8px 16px;border:none;border-radius:6px;font-weight:bold;margin-right:8px;">🔄 Force Render</button>' +
          '<button onclick="try{if(typeof state!==\\'undefined\\'&&!state.records.length)state.records=[{id:\\'SKU-001\\',name:\\'Test\\',price:1000,cost:600,stock:50}];render()}catch(e){alert(e.message)}" style="background:#3b82f6;color:#fff;padding:8px 16px;border:none;border-radius:6px;font-weight:bold;margin-right:8px;">➕ Add Test Data</button>' +
          '<button onclick="document.getElementById(\\'diagOverlay\\').remove()" style="background:#64748b;color:#fff;padding:8px 16px;border:none;border-radius:6px;font-weight:bold;">✖ Close</button>' +
          '</div>';
        
        var old = document.getElementById('diagOverlay');
        if (old) old.remove();
        document.body.appendChild(diag);
      }
    } catch(e) { alert('Diagnostic error: ' + e.message); }
  }
  
  // Yeroo app banamu fi yeroo hunda
  setTimeout(showDiag, 2000);
  setTimeout(showDiag, 5000);
  setInterval(showDiag, 8000);
})();
</script>
'''

# Yoo diagnostic hin jiraanne, </body> dura galchi
if 'VISIBLE DIAGNOSTIC OVERLAY' not in content:
    content = content.replace('</body>', diag + '\n</body>')
    with open(html_path, 'w') as f:
        f.write(content)
    print("✅ VISIBLE DIAGNOSTIC OVERLAY dabalameera!")
else:
    print("⚠️  Diagnostic amma jira.")

print("📍 Hojii xumurameera!")

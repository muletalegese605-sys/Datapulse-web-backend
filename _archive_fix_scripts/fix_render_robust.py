import os, re

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    content = f.read()

# render() function guutuu bakka bu'i - nageenya qabu, content duwwaa akka hin taane
new_render = '''function render(){
  var el = document.getElementById('main');
  if (!el) { var app = document.getElementById('app'); if (app) { el = app.querySelector('main') || app; if (!el.id) el.id = 'main'; } }
  if (!el) return;
  
  try { if (!state.tab) state.tab = 'dashboard'; } catch(e){}
  try { if (!state.org) state.org = {id:'ORG-DEMO', name:'Demo Enterprise'}; } catch(e){}
  try { if (!state.user) state.user = {name:'Demo Admin', email:'demo@datapulse.com', role:'admin'}; } catch(e){}
  try { if (!Array.isArray(state.records)) state.records = []; } catch(e){}
  
  try { var hdr = document.getElementById('hdrOrg'); if (hdr) hdr.textContent = (state.org && state.org.name) || 'Demo Enterprise'; } catch(e){}
  try { if (typeof updateTrialBadge === 'function') updateTrialBadge(); } catch(e){}
  
  var k = {};
  try { k = kpis(); } catch(e) { console.warn('kpis error:', e.message); }
  
  try {
    switch(state.tab){
      case 'dashboard': el.innerHTML = (typeof vDash === 'function') ? vDash(k) : '<div class="p-4">Dashboard loading...</div>'; if (typeof drawDashChart === 'function') drawDashChart(); break;
      case 'sources': el.innerHTML = vSources(); break;
      case 'capabilities': el.innerHTML = vCaps(); break;
      case 'automate': el.innerHTML = vAuto(); break;
      case 'contracts': el.innerHTML = vContracts(); break;
      case 'ai': el.innerHTML = vAi(); if (typeof drawAiMessages === 'function') drawAiMessages(); break;
      case 'charts': el.innerHTML = vChartsShell(); if (typeof drawMainChart === 'function') drawMainChart(); break;
      case 'audit': el.innerHTML = vAudit(); break;
      case 'orgs': el.innerHTML = vOrgs(); break;
      case 'perms': el.innerHTML = vPerms(); break;
      case 'report': el.innerHTML = vReport(k); break;
      case 'contact': el.innerHTML = vContact(); break;
      default: el.innerHTML = (typeof vDash === 'function') ? vDash(k) : '<div class="p-4">Dashboard</div>';
    }
  } catch(e) {
    console.error('Render switch error:', e.message);
    el.innerHTML = '<div class="p-4 bg-rose-500/10 border border-rose-500/30 rounded-xl"><p class="text-rose-400 text-xs">Render error: ' + e.message + '</p></div>';
  }
  
  try { if (typeof DP !== 'undefined' && DP.i18n && DP.i18n.apply) DP.i18n.apply(); } catch(e){}
  try { if (window.DP && DP.api && DP.api.loadAll && !window._dpLoading) { window._dpLoading = true; DP.api.loadAll().finally(function(){ window._dpLoading = false; }); } } catch(e){}
}'''

# render() function duraa barbaadii, kan haaraa galchi
pattern = re.compile(r'function render\(\)\s*\{', re.MULTILINE)
match = pattern.search(content)
if match:
    # Bracket dhiphinaa barbaadii, function guutuu bakka buusi
    start = match.start()
    brace_count = 0
    end = start
    for i in range(match.end() - 1, len(content)):
        if content[i] == '{':
            brace_count += 1
        elif content[i] == '}':
            brace_count -= 1
            if brace_count == 0:
                end = i + 1
                break
    content = content[:start] + new_render + content[end:]
    print("✅ render() function guutummaatti sirreeffameera!")
else:
    print("❌ render() function hin argamne!")

with open(html_path, 'w') as f:
    f.write(content)

print("📍 Hojii xumurameera!")

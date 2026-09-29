import os, re

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    content = f.read()

# quickDemoLogin function guutuu bakka buusi - nageenya qabu
new_fn = '''function quickDemoLogin(){
  try{
    localStorage.setItem('dp_demo_user', JSON.stringify({name:'Demo Admin',email:'demo@datapulse.com',role:'admin'}));
    var lp=document.getElementById('landingPage'); if(lp) lp.classList.add('hidden');
    var ls=document.getElementById('loginScreen'); if(ls) ls.classList.add('hidden');
    var app=document.getElementById('app'); if(app){app.classList.remove('hidden');app.style.display='';app.removeAttribute('hidden');}
    var main=document.getElementById('main'); if(main){main.classList.remove('hidden');main.style.display='';main.removeAttribute('hidden');}
    if(typeof state!=='undefined'){
      state.user={name:'Demo Admin',email:'demo@datapulse.com',role:'admin'};
      state.org={id:'ORG-DEMO',name:'Demo Enterprise'};
      if(!state.tab) state.tab='dashboard';
      if(!Array.isArray(state.records)) state.records=[];
    }
    if(typeof render==='function'){
      try{ render(); }catch(re){ main.innerHTML='<div style="padding:20px;color:#ef4444;font-family:monospace;font-size:12px;"><b>render() error:</b><br>'+re.message+'</div>'; }
    }
    try{ if(typeof DP!=='undefined'&&DP.api&&DP.api.loadAll) DP.api.loadAll(); }catch(e){}
    if(typeof toast==='function') toast('Demo login successful','success');
  }catch(e){
    alert('quickDemoLogin error: '+e.message);
  }
}'''

# Bakka function duraa jiru, kan haaraa galchi
pattern = re.compile(r'function\s+quickDemoLogin\s*\(\s*\)\s*\{', re.MULTILINE)
m = pattern.search(content)
if m:
    # Brace balance fayyadamuun, function guutuu barbaadi
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
    content = content[:start] + new_fn + content[end:]
    print("✅ quickDemoLogin function guutummaatti bakka bu'ameera!")
else:
    print("❌ Function hin argamne!")

with open(html_path, 'w') as f:
    f.write(content)

# Mirkaneessi
with open(html_path, 'r') as f:
    new_content = f.read()

print(f"\n📍 MIRKANEESSA:")
print(f"   quickDemoLogin: {len(re.findall(r'function quickDemoLogin', new_content))}")
print(f"   DP.api references in function: {'HIN QABU ✅' if 'DP.api.loadAll' not in new_content[new_content.find('function quickDemoLogin'):new_content.find('function quickDemoLogin')+1500] else 'AMMAS JIRA'}")

# Script balance
print(f"   <script>: {len(re.findall(r'<script', new_content))}, </script>: {new_content.count('</script>')}")

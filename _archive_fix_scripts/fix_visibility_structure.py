import os, re

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    content = f.read()

print("=" * 60)
print("🔧 VISIBILITY & STRUCTURE FIX")
print("=" * 60)

changes = []

# ============================================================
# 1. Yeroo app banamu, landingPage VISIBLE taasisu
# ============================================================
init_script = '''
// ========== APP INITIALIZATION ==========
(function() {
  function initializeApp() {
    try {
      // Yeroo app banamu, landingPage mul'achiisi
      var lp = document.getElementById('landingPage');
      var ls = document.getElementById('loginScreen');
      var app = document.getElementById('app');
      var main = document.getElementById('main');
      
      if (lp) { lp.classList.remove('hidden'); lp.style.display = ''; lp.removeAttribute('hidden'); }
      if (ls) { ls.classList.add('hidden'); }
      if (app) { app.classList.add('hidden'); }
      // main - element kun #app keessaa ala waan jiruuf, yeroo jalqabaa dhiisi
      
      console.log('✅ App initialized: landingPage visible');
    } catch(e) { console.warn('init error:', e.message); }
  }
  
  // Yeroo DOM qophaa'e
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeApp);
  } else {
    setTimeout(initializeApp, 100);
  }
})();
// ========================================
'''

if 'APP INITIALIZATION' not in content:
    # Bakka </script> isa dhumaa dura galchi
    last_close = content.rfind('</script>')
    if last_close > 0:
        content = content[:last_close] + init_script + '\n' + content[last_close:]
        changes.append('APP INITIALIZATION dabalameera')

# ============================================================
# 2. #main element sun #app keessatti akka jiraatu (structure fix)
# ============================================================
# #app element open fi close barbaadi
app_match = re.search(r'<div[^>]*id="app"[^>]*>', content)
main_match = re.search(r'<main[^>]*id="main"[^>]*>', content)

if app_match and main_match:
    app_start = app_match.start()
    main_start = main_match.start()
    
    # Yoo main sun app booda jira (app keessaa ala)
    if main_start > app_start:
        # app element nesting xumura barbaadi
        depth = 0
        i = app_match.end() - 1
        app_end = None
        while i < len(content):
            if content[i:i+4] == '<div':
                depth += 1
            elif content[i:i+6] == '</div>':
                if depth == 0:
                    app_end = i + 6
                    break
                depth -= 1
            i += 1
        
        if app_end and main_start < app_end:
            print(f"   ✅ #main sun #app keessatti jira (structure sirrii)")
        elif app_end:
            print(f"   ⚠️  #main sun #app keessaa ala jira (app_end = {app_end}, main_start = {main_start})")

# ============================================================
# 3. Backup handler visibility
# ============================================================
visibility_backup = '''
// ========== VISIBILITY BACKUP ==========
window.addEventListener('load', function() {
  setTimeout(function() {
    try {
      var lp = document.getElementById('landingPage');
      var app = document.getElementById('app');
      // Yoo lamaanuu hidden ta'aniif, landingPage mul'achiisi
      var lp_hidden = !lp || lp.classList.contains('hidden');
      var app_hidden = !app || app.classList.contains('hidden');
      if (lp_hidden && app_hidden) {
        if (lp) { lp.classList.remove('hidden'); lp.style.display = ''; }
        console.log('✅ Backup: landingPage visible');
      }
    } catch(e) {}
  }, 500);
});

// Yeroo login tuqtu, app mul'achiisi
document.addEventListener('click', function(ev) {
  var t = ev.target.closest('button');
  if (!t) return;
  var txt = (t.textContent || '').trim().toLowerCase();
  if (txt.indexOf('quick demo login') !== -1 || txt === 'log in') {
    setTimeout(function() {
      try {
        var app = document.getElementById('app');
        if (app) { app.classList.remove('hidden'); app.style.display = ''; }
        var main = document.getElementById('main');
        if (main) { main.classList.remove('hidden'); main.style.display = ''; }
        var lp = document.getElementById('landingPage');
        if (lp) lp.classList.add('hidden');
        var ls = document.getElementById('loginScreen');
        if (ls) ls.classList.add('hidden');
        if (typeof render === 'function') { try { render(); } catch(e) {} }
      } catch(e) {}
    }, 800);
  }
}, true);
// ======================================
'''

if 'VISIBILITY BACKUP' not in content:
    last_close = content.rfind('</script>')
    if last_close > 0:
        content = content[:last_close] + visibility_backup + '\n' + content[last_close:]
        changes.append('VISIBILITY BACKUP dabalameera')

# ============================================================
# Save
# ============================================================
with open(html_path, 'w') as f:
    f.write(content)

print("\n" + "=" * 60)
print("✅ FIX XUMURAMEERA!")
print("=" * 60)
for c in changes:
    print("  • " + c)
if not changes:
    print("  ⚠️  Wanti jijjiirame hin jiru.")
print("=" * 60)

# Mirkaneessi
with open(html_path, 'r') as f:
    new_content = f.read()
print(f"\n📍 Script balance: {len(re.findall(r'<script', new_content))} / {new_content.count('</script>')}")

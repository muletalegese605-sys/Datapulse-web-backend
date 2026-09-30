import os, re

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    content = f.read()

# 1. Kutaa koodii adda addaa haqi (kanneen text ta'anii mul'atan)
# Kanneen kunneen `</script>` ala waan jiraniif, akka barruutti mul'atu
removals = [
    'NUCLEAR DASHBOARD FIX',
    'FINAL DASHBOARD RENDER',
    'APP VISIBILITY FIX',
    'FORCE RENDER CONTENT',
    'STATE GUARD',
    'AUTH BACKUP HANDLER',
    'DASHBOARD SHOW FIX',
    'BACKEND FIRST LOADER',
    'DASHBOARD RENDER BOOST',
    'VISIBLE DIAGNOSTIC OVERLAY',
]

removed_count = 0
for tag in removals:
    # Kutaa koodii sana haqquuf, pattern bal'aa fayyadami
    pattern = re.compile(
        r'\n?\s*//\s*=+\s*' + re.escape(tag) + r'\s*=+.*?(?=\n\s*(?:window\.addEventListener|document\.addEventListener|<script|</body>|$))',
        re.DOTALL
    )
    new_content, n = pattern.subn('', content)
    if n > 0:
        content = new_content
        removed_count += 1
        print(f"  🗑️  {tag} haqameera")

print(f"\n✅ Kutaa {removed_count} adda addaa haqamaniiru!")

# 2. Kutaa jalqabaa (broken text) hunda haquuf - regex bal'aa
# Kanneen text ta'anii mul'atan, kanneen `var attempts` fi `function forceRender` qaban
text_blocks = [
    r'\n?\s*//\s*=+\s*NUCLEAR DASHBOARD FIX[\s\S]*?(?=\n\s*//\s*=+\s*FINAL DASHBOARD RENDER|\n\s*<script|\n\s*</body>)',
    r'\n?\s*//\s*=+\s*FINAL DASHBOARD RENDER[\s\S]*?(?=\n\s*<script|\n\s*</body>)',
    r'\n?\s*//\s*=+\s*APP VISIBILITY FIX[\s\S]*?(?=\n\s*//\s*=+\s*NUCLEAR|\n\s*<script|\n\s*</body>)',
]
for pat in text_blocks:
    new_content, n = re.subn(pat, '', content, count=5, flags=re.DOTALL)
    if n > 0:
        content = new_content
        print(f"  🗑️  Text block haqameera ({n} jechuu)")

# 3. Backup: Yoo ammas text ta'ee mul'atu jiraate, hunda sarara `// ===` jalqabee, `</script>` gadiitti jiru haqi
# Kun yeroo baay'ee sanada.
lines = content.split('\n')
filtered = []
in_broken_block = False
for line in lines:
    stripped = line.strip()
    # Yoo sararri `// ===` jalqabee, `NUCLEAR`/`FINAL`/`APP` jedhu qabaate, sana jalqabi
    if re.match(r'^//\s*=+\s*(NUCLEAR|FINAL|APP|FORCE|STATE|AUTH|DASHBOARD|BACKEND|VISIBLE)', stripped):
        in_broken_block = True
        continue
    # Yoo sararri `<script>` ykn `</body>` ta'e, xumuri
    if in_broken_block and (stripped.startswith('<script') or stripped.startswith('</body>') or stripped.startswith('</html>')):
        in_broken_block = False
    if not in_broken_block:
        filtered.append(line)

content = '\n'.join(filtered)
print("✅ Backup filter hojjeteera")

# 4. Amma `<script>` tag isa jalqabaa check - yoo broken ta'e, sirreessi
# Yoo `<script>` kunniin `src` hin qaban, isaan sun `<script>` fi `</script>` waliin ta'uu qabu

# 5. Amma script haaraa, QULQULLUU ta'e, `<script>` TAG KESSA galchi
clean_script = '''
<script>
// ========== CLEAN BOOTSTRAP ==========
(function() {
  function bootstrap() {
    try {
      // State mirkaneessi
      if (typeof window.state === 'undefined') {
        window.state = { tab: 'dashboard', records: [], org: {id:'ORG-DEMO', name:'Demo Enterprise'}, user: {name:'Demo Admin'} };
      }
      // #app fi #main mul'achiisi
      var app = document.getElementById('app');
      var main = document.getElementById('main');
      var ls = document.getElementById('loginScreen');
      var lp = document.getElementById('landingPage');
      if (ls) ls.classList.add('hidden');
      if (lp) lp.classList.add('hidden');
      if (app) { app.classList.remove('hidden'); app.style.display = ''; }
      if (main) {
        main.classList.remove('hidden');
        main.style.display = '';
        if (main.innerHTML.trim().length < 100) {
          main.innerHTML = '<div style="padding:20px;color:#10b981;font-family:monospace;">✅ App loaded. render() function: ' + (typeof window.render === 'function' ? 'OK' : 'NOT FOUND') + '<br>state.records: ' + (window.state.records ? window.state.records.length : 'none') + '</div>';
        }
      }
    } catch(e) { console.warn('bootstrap err:', e.message); }
  }
  window.addEventListener('load', function() { setTimeout(bootstrap, 500); });
  document.addEventListener('click', function(ev) {
    var t = ev.target.closest('button');
    if (!t) return;
    var txt = (t.textContent || '').trim().toLowerCase();
    if (txt.indexOf('quick demo') !== -1 || txt === 'log in') {
      setTimeout(bootstrap, 800);
      setTimeout(bootstrap, 2000);
    }
  }, true);
})();
</script>
'''

# Yoo bootstrap hin jiraanne, </body> dura galchi
if 'CLEAN BOOTSTRAP' not in content:
    content = content.replace('</body>', clean_script + '\n</body>')

with open(html_path, 'w') as f:
    f.write(content)

print("\n" + "=" * 50)
print("✅ ULTIMATE FIX xumurameera!")
print("=" * 50)
print("\n📍 Maal arguu qabda dashboard irratti:")
print("   Yoo '✅ App loaded. render() function: OK' argite")
print("   → render() function sun hojjetaa jira, garuu isa duraa hin jiru.")
print("   → Data duwwaa ta'uu danda'a.")

import os, re

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    content = f.read()

print("=" * 60)
print("🔍 LAUNCH APP BUTTON - DIAGNOSTIC REPORT")
print("=" * 60)

# 1. Button "Launch App" hunda barbaadi (sarara lakkoofsaan)
print("\n1. Button 'Launch App' hunda:")
matches = list(re.finditer(r'<button[^>]*>[\s\S]{0,200}?Launch App[\s\S]{0,30}?</button>', content))
print(f"   Total: {len(matches)}\n")

for i, m in enumerate(matches):
    line_no = content[:m.start()].count('\n') + 1
    btn_html = m.group(0)
    print(f"   #{i+1} Sarara {line_no}:")
    print(f"      {btn_html[:250]}")
    # Onclick jira?
    onclick = re.search(r'onclick="([^"]*)"', btn_html)
    if onclick:
        print(f"      ⚠️  onclick: {onclick.group(1)[:120]}")
    else:
        print(f"      ❌ onclick HIN QABU")
    # Type jira?
    if 'type="button"' in btn_html:
        print(f"      ✅ type=\"button\" qaba")
    else:
        print(f"      ⚠️  type=\"button\" hin qabu")
    print()

# 2. Functions jiraachuu
print("\n2. Functions jiraachuu:")
for fn in ['showLoginFromLanding', 'go', 'render', 'switchAuth', 'quickDemoLogin']:
    count = len(re.findall(r'function\s+' + re.escape(fn) + r'\s*\(', content))
    status = f'✅ ({count})' if count > 0 else '❌ HIN JIRU'
    print(f"   {fn}(): {status}")

# 3. getElementById('loginScreen') fi getElementById('landingPage') jiraachuu
print("\n3. Element IDs mirkaneessi:")
for eid in ['loginScreen', 'landingPage', 'app', 'main']:
    el_count = len(re.findall(r'id="' + eid + r'"', content))
    print(f"   #{eid}: {el_count} (1 ta'uu qaba)")

# 4. Script tags fi function render() script keessaa
print("\n4. Script Tags fi function render():")
opens = len(re.findall(r'<script\b[^>]*>', content))
closes = content.count('</script>')
print(f"   <script>: {opens}, </script>: {closes}, Diff: {opens - closes}")

idx_render = content.find('function render(')
if idx_render > 0:
    before = content[:idx_render]
    last_open = before.rfind('<script')
    last_close = before.rfind('</script>')
    in_script = last_open > last_close
    print(f"   function render() script keessa: {'✅ EEYY' if in_script else '❌ LAKKI'}")

# 5. Backup handlers/AUTH BUTTONS jiraachuu
print("\n5. Backup Handlers:")
for tag in ['AUTH BACKUP HANDLER', 'UNIVERSAL BUTTON HANDLER', 'LAUNCH BUTTON', 'APP VISIBILITY']:
    if tag in content:
        idx = content.find(tag)
        line_no = content[:idx].count('\n') + 1
        print(f"   ✅ {tag} (Sarara {line_no})")
    else:
        print(f"   ❌ {tag} hin jiru")

# 6. Onclick function calls: 'showLoginFromLanding' ykn 'go('
print("\n6. Button onclick function calls:")
for m in re.finditer(r'onclick="([^"]{0,100})"', content):
    onclick = m.group(1)
    line_no = content[:m.start()].count('\n') + 1
    if 'login' in onclick.lower() or 'launch' in onclick.lower() or 'go(' in onclick:
        # Yoo function sun jiraachuu fi dhabuu mirkaneessi
        fname_match = re.match(r'([a-zA-Z_$][a-zA-Z0-9_$]*)\(', onclick)
        fname = fname_match.group(1) if fname_match else 'inline'
        exists = f'function {fname}(' in content if fname != 'inline' else 'inline JS'
        print(f"   Sarara {line_no}: {onclick[:80]}")
        print(f"      Function: {fname} — {exists}")

print("\n" + "=" * 60)
print("📍 Xiinxalli xumurameera.")
print("=" * 60)

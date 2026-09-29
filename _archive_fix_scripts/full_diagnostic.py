import os, re

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    content = f.read()

print("=" * 65)
print("🔍 DATAPULSE — QORANNOO GUUTUU (FULL DIAGNOSTIC)")
print("=" * 65)

# ============================================================
# 1. FILE STATS
# ============================================================
print("\n📁 1. FILE STATS")
print(f"   File size: {len(content):,} bytes")
print(f"   Total lines: {content.count(chr(10)):,}")

# ============================================================
# 2. ELEMENTS HUNDA (jiraachuu fi visibility)
# ============================================================
print("\n📋 2. ELEMENTS (jiraachuu fi visibility)")
elements = ['landingPage', 'loginScreen', 'app', 'main', 'tbLogin', 'tbRegister',
            'loginForm', 'regForm', 'loginEmail', 'loginPass', 'btnLogin', 'main']
for eid in elements:
    matches = list(re.finditer(r'<(\w+)[^>]*id="' + re.escape(eid) + r'"[^>]*>', content))
    if not matches:
        print(f"   ❌ #{eid}: HIN JIRU")
    elif len(matches) > 1:
        print(f"   ⚠️  #{eid}: {len(matches)} (DUPLICATE!)")
    else:
        m = matches[0]
        tag = m.group(1)
        line_no = content[:m.start()].count('\n') + 1
        cls_match = re.search(r'class="([^"]*)"', m.group(0))
        cls = cls_match.group(1) if cls_match else ''
        hidden = 'hidden' in cls
        status = '🔴 HIDDEN' if hidden else '🟢 VISIBLE'
        print(f"   ✅ #{eid} ({tag}, Sarara {line_no}): {status}")

# ============================================================
# 3. FUNCTIONS HUNDA
# ============================================================
print("\n⚙️  3. FUNCTIONS")
functions = ['showLoginFromLanding', 'quickDemoLogin', 'switchAuth', 'go',
             'render', 'doLogin', 'vDash', 'kpis', 'toast', 'forceShowApp']
for fn in functions:
    count = len(re.findall(r'function\s+' + re.escape(fn) + r'\s*\(', content))
    if count == 0:
        print(f"   ❌ {fn}(): HIN JIRU")
    elif count > 1:
        print(f"   ⚠️  {fn}(): {count} (DUPLICATE!)")
    else:
        m = re.search(r'function\s+' + re.escape(fn) + r'\s*\(', content)
        line_no = content[:m.start()].count('\n') + 1
        # Script keessa?
        before = content[:m.start()]
        last_open = before.rfind('<script')
        last_close = before.rfind('</script>')
        in_script = last_open > last_close
        print(f"   ✅ {fn}() (Sarara {line_no}): script={'✅' if in_script else '❌ ALAAAA'}")

# ============================================================
# 4. SCRIPT TAGS
# ============================================================
print("\n📜 4. SCRIPT TAGS")
opens = len(re.findall(r'<script\b[^>]*>', content))
closes = content.count('</script>')
print(f"   <script>: {opens}")
print(f"   </script>: {closes}")
print(f"   Balance: {'✅' if opens == closes else '❌ DOGOGGORA (diff: ' + str(opens - closes) + ')'}")

# Inline scripts
inline = re.findall(r'<script\b(?![^>]*\bsrc=)[^>]*>', content)
print(f"   Inline scripts: {len(inline)}")

# ============================================================
# 5. BUTTONS HUNDA (onclick handlers)
# ============================================================
print("\n🔘 5. BUTTONS (onclick)")
buttons = re.findall(r'<button[^>]*>[\s\S]{0,200}?</button>', content)
print(f"   Total buttons: {len(buttons)}")

with_onclick = 0
without_onclick = 0
type_button = 0
type_submit = 0
type_missing = 0

for m in re.finditer(r'<button[^>]*>', content):
    tag = m.group(0)
    if 'onclick=' in tag:
        with_onclick += 1
    else:
        # Yoo button sun 'Log In' ykn 'Create Organization' ta'e, submit waliin ta'uu danda'a
        without_onclick += 1
    if 'type="button"' in tag:
        type_button += 1
    elif 'type="submit"' in tag:
        type_submit += 1
    else:
        type_missing += 1

print(f"   onclick qabu: {with_onclick}")
print(f"   onclick hin qabne: {without_onclick}")
print(f"   type=\"button\": {type_button}")
print(f"   type=\"submit\": {type_submit}")
print(f"   type hin qabne: {type_missing}")

# ============================================================
# 6. BACKUP HANDLERS
# ============================================================
print("\n🛡️  6. BACKUP HANDLERS")
handlers = ['AUTH BACKUP HANDLER', 'UNIVERSAL BUTTON HANDLER', 'LAUNCH BUTTON',
            'APP VISIBILITY', 'VISIBILITY BACKUP', 'SHOWLOGIN BACKUP HANDLER',
            'CLICK DIAGNOSTIC', 'APP INITIALIZATION']
for h in handlers:
    if h in content:
        idx = content.find(h)
        line_no = content[:idx].count('\n') + 1
        print(f"   ✅ {h} (Sarara {line_no})")
    else:
        print(f"   ❌ {h}")

# ============================================================
# 7. STATE VARIABLE
# ============================================================
print("\n💾 7. STATE VARIABLE")
state_assigns = list(re.finditer(r'(?:var|let|const|window\.)\s*state\s*=', content))
print(f"   state assignments: {len(state_assigns)}")
for m in state_assigns:
    line_no = content[:m.start()].count('\n') + 1
    print(f"      Sarara {line_no}")

# ============================================================
# 8. ORPHANED JS CODE (text ta'ee mul'atu)
# ============================================================
print("\n🚨 8. ORPHANED JS CODE")
orphan_patterns = [
    ('forceRender', r'\bforceRender\b'),
    ('bootstrap', r'\bbootstrap\b'),
    ('Yeroo login/demo', r'// Yeroo login/demo'),
    ('setInterval orphans', r'setInterval\(\(\)\s*=>'),
    ('function startTicker', r'function startTicker'),
]
found_orphans = 0
for name, pat in orphan_patterns:
    matches = list(re.finditer(pat, content))
    if matches:
        # Script keessa jira?
        orphan_count = 0
        for m in matches:
            before = content[:m.start()]
            last_open = before.rfind('<script')
            last_close = before.rfind('</script>')
            in_script = last_open > last_close
            if not in_script:
                orphan_count += 1
        if orphan_count > 0:
            print(f"   ❌ {name}: {orphan_count} (script ALAAAA — text ta'ee mul'ata!)")
            found_orphans += orphan_count
        else:
            print(f"   ✅ {name}: {len(matches)} (script keessa)")
if found_orphans == 0:
    print("   ✅ Orphaned code hin jiru!")

# ============================================================
# 9. DP OBJECTS
# ============================================================
print("\n🌐 9. DP OBJECTS")
for obj in ['DP.api', 'DP.usage', 'DP.permissions', 'DP.theme', 'DP.i18n']:
    count = content.count(obj)
    print(f"   {obj}: {count}")

# ============================================================
# 10. CONTENT CHECK
# ============================================================
print("\n📊 10. DASHBOARD CONTENT")
dash_match = re.search(r'id="main"[^>]*>([\s\S]{0,300})', content)
if dash_match:
    content_len = len(dash_match.group(1).strip())
    print(f"   #main keessaa content: {content_len} chars")
    if content_len < 50:
        print(f"   ⚠️  Dashboard content duwwaa ta'uu danda'a")
else:
    print(f"   ❌ #main element hin argamne")

# ============================================================
# CUUNFAA
# ============================================================
print("\n" + "=" * 65)
print("📌 CUUNFAA")
print("=" * 65)

issues = []

# Elements check
missing_els = []
dup_els = []
for eid in ['landingPage', 'loginScreen', 'app', 'main']:
    c = len(re.findall(r'id="' + eid + r'"', content))
    if c == 0: missing_els.append(eid)
    elif c > 1: dup_els.append(eid)

if missing_els: issues.append(f"Elements hir'atan: {', '.join(missing_els)}")
if dup_els: issues.append(f"Elements duplicate: {', '.join(dup_els)}")

# Functions check
missing_fns = []
for fn in ['showLoginFromLanding', 'quickDemoLogin', 'render', 'switchAuth']:
    if f'function {fn}(' not in content:
        missing_fns.append(fn)
if missing_fns: issues.append(f"Functions hir'atan: {', '.join(missing_fns)}")

# Script balance
if opens != closes: issues.append(f"Script tags balance: {opens}/{closes}")

# Orphaned code
if found_orphans > 0: issues.append(f"Orphaned JS code: {found_orphans}")

# Buttons
if type_missing > 0: issues.append(f"Buttons type hin qabne: {type_missing}")

if issues:
    print("\n⚠️  RAKKOOWWAN ARGAMAN:")
    for i, issue in enumerate(issues, 1):
        print(f"   {i}. {issue}")
    print("\n💡 Furmaata barbaaduuf, comandiin kun galchi:")
    print("   python3 <fix_script.py>")
else:
    print("\n🎉 RAKKOON GUDDAAN HIN JIRU!")
    print("   App kee guutummaatti sirrii ta'uu danda'a.")

print("\n" + "=" * 65)
print("📍 Xiinxalli xumurameera.")
print("=" * 65)

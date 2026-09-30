import os, re

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    content = f.read()

print("=" * 60)
print("🔍 ELEMENT IDs VERIFICATION")
print("=" * 60)

# Critical elements hunda - id fi tag type
critical = {
    'landingPage': 'div',
    'loginScreen': 'div',
    'app': 'div',
    'main': 'main',
    'tbLogin': 'button',
    'tbRegister': 'button',
    'loginForm': 'form',
    'regForm': 'form',
    'loginEmail': 'input',
    'loginPass': 'input',
    'main': 'main',
}

print("\n1. Element IDs hunda mirkaneessi:")
missing = []
duplicates = []

for eid in critical:
    # Element hunda barbaadi (tag kamiyyuu)
    pattern = re.compile(r'<(\w+)[^>]*id="' + re.escape(eid) + r'"[^>]*>', re.IGNORECASE)
    matches = pattern.findall(content)
    count = len(matches)
    
    if count == 0:
        status = '❌ HIN JIRU'
        missing.append(eid)
    elif count == 1:
        status = '✅ 1'
    else:
        status = f'⚠️  {count} (DUPLICATE!)'
        duplicates.append(eid)
    
    # Sarara lakkoofsa
    m = re.search(r'<(\w+)[^>]*id="' + re.escape(eid) + r'"[^>]*>', content, re.IGNORECASE)
    if m:
        line_no = content[:m.start()].count('\n') + 1
        tag_type = m.group(1).lower()
        print(f"   #{eid:<16} ({tag_type:<7}): Sarara {line_no:<5} {status}")
    else:
        print(f"   #{eid:<16}: {status}")

# 2. Critical elements fi section rakkoo
print("\n2. Hir'ina jiru (missing):")
if missing:
    for eid in missing:
        print(f"   ❌ #{eid}")
else:
    print("   ✅ Hir'inni hin jiru — hundi jiran!")

print("\n3. Duplicates:")
if duplicates:
    for eid in duplicates:
        print(f"   ⚠️  #{eid}")
else:
    print("   ✅ Duplicate hin jiru!")

# 4. Structure: #main eessa jira? (#app keessa? landingPage keessa?)
print("\n4. Structure:")
for eid in ['landingPage', 'loginScreen', 'app', 'main']:
    m = re.search(r'<(\w+)[^>]*id="' + eid + r'"[^>]*>', content, re.IGNORECASE)
    if m:
        # Dursaa (500 chars) ilaali - maal keessa jira?
        before = content[max(0, m.start()-1000):m.start()]
        # Element open tags barbaadi
        opens = re.findall(r'<(\w+)[^>]*id="([^"]+)"', before)
        # Element isa dhumaa
        last_id = opens[-1][1] if opens else 'body'
        # Yoo 'landingPage' fi 'loginScreen' fi 'app' isa duraa jiran, sana agarsiisi
        print(f"   #{eid}: {last_id} keessatti")

# 5. Element visibility
print("\n5. Visibility (hidden/class):")
for eid in ['landingPage', 'loginScreen', 'app', 'main']:
    m = re.search(r'<(\w+)[^>]*id="' + eid + r'"[^>]*class="([^"]*)"', content, re.IGNORECASE)
    if m:
        cls = m.group(2)
        hidden = 'hidden' in cls
        status = '🔴 HIDDEN' if hidden else '🟢 VISIBLE'
        print(f"   #{eid}: {status} (class: {cls[:60]})")
    else:
        m2 = re.search(r'<(\w+)[^>]*id="' + eid + r'"[^>]*>', content, re.IGNORECASE)
        if m2:
            print(f"   #{eid}: 🟢 VISIBLE (class hin qabu)")
        else:
            print(f"   #{eid}: ❌ HIN JIRU")

print("\n" + "=" * 60)
print("📍 Xiinxalli xumurameera.")
print("=" * 60)

# 6. Yoo elements hir'atan jiraatan, furmaata kennii
if missing:
    print("\n⚠️  ELEMENTS HIR'ATAN JIRU!")
    print("   Comandii kun elements hir'atan bakka isaanii galcha:")
    print("   python3 restore_missing_elements.py")
else:
    print("\n✅ ELEMENTS HUNDI JIRU!")
    print("   Rakkoon kun element dhabuu MITI.")
    print("   Rakkoon kun JavaScript code keessa jiraachuu danda'a.")

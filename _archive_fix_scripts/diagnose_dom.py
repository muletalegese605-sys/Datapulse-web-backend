import os, re

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    content = f.read()

print("=" * 55)
print("🔍 DOM STRUCTURE DIAGNOSTIC")
print("=" * 55)

# 1. #app element - maal akka qabu
print("\n1. #app Element (attributes):")
m = re.search(r'<[^>]*id="app"[^>]*>', content)
if m:
    print(f"   {m.group(0)}")
else:
    print("   ❌ HIN JIRU")

# 2. #main element - maal akka qabu
print("\n2. #main Element (attributes):")
m = re.search(r'<[^>]*id="main"[^>]*>', content)
if m:
    print(f"   {m.group(0)}")
    # #main duraa maal akka jiru ilaali
    start = m.start()
    before = content[max(0, start-500):start]
    print("\n   === #main duraa (500 chars) ===")
    print("   " + before[-400:].replace('\n', '\n   '))
else:
    print("   ❌ HIN JIRU")

# 3. Nuclear fix jiraachuu
print("\n3. NUCLEAR FIX jiraachuu:")
if 'NUCLEAR DASHBOARD FIX' in content:
    print("   ✅ NUCLEAR FIX ni jira")
else:
    print("   ❌ NUCLEAR FIX hin jiru!")

# 4. <script> tags
print("\n4. Script Tags:")
for i, m in enumerate(re.finditer(r'<script[^>]*>', content)):
    line_no = content[:m.start()].count('\n') + 1
    print(f"   • Sarara {line_no}: {m.group(0)}")

# 5. Closing script tags count
print(f"\n5. </script> tags: {content.count('</script>')}")

# 6. CSS: [hidden] attribute
print("\n6. CSS [hidden] rules:")
for m in re.finditer(r'\[hidden\][^{]*\{[^}]*\}', content):
    print(f"   • {m.group(0)[:100]}")

# 7. Landing page structure - #landingPage maal akka qabu
print("\n7. #landingPage Element:")
m = re.search(r'<[^>]*id="landingPage"[^>]*>', content)
if m:
    print(f"   {m.group(0)}")

# 8. #loginScreen element
print("\n8. #loginScreen Element:")
m = re.search(r'<[^>]*id="loginScreen"[^>]*>', content)
if m:
    print(f"   {m.group(0)}")

# 9. #main first 200 chars of content
print("\n9. #main keessaa (200 chars):")
m = re.search(r'id="main"[^>]*>', content)
if m:
    rest = content[m.end():m.end()+200]
    print(f"   {rest}")

print("\n" + "=" * 55)
print("📍 Xiinxalli xumurameera.")
print("=" * 55)

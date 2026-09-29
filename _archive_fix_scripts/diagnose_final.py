import os, re

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    content = f.read()

print("=" * 55)
print("🔍 DATAPULSE DIAGNOSTIC REPORT")
print("=" * 55)

# 1. render() function lakkoofsa
count = content.count('function render(')
print(f"\n1. 'function render(' lakkoofsa: {count}")
if count > 1:
    print("   ⚠️  RAKKOO: render() function lamaan jiru! Kun walitti bu'iinsa uuma.")
else:
    print("   ✅ render() function tokko qofa jira.")

# 2. #main, #app, #dashboard jiraachuu fi hidden ta'uu
print("\n2. Element Structure:")
for eid in ['main', 'app', 'dashboard', 'loginScreen']:
    m = re.search(r'id="' + eid + r'"[^>]*', content)
    if m:
        line = m.group(0)
        hidden = 'hidden' in line
        print(f"   • #{eid}: {'🔴 HIDDEN' if hidden else '🟢 VISIBLE'}")
    else:
        print(f"   • #{eid}: ❌ HIN JIRU")

# 3. onclick handlers maal akka qaban
print("\n3. Button onclick handlers:")
for m in re.finditer(r'<button[^>]*onclick="([^"]{0,120})[^"]*"', content):
    onclick = m.group(1)
    if 'loginForm' in onclick or 'regForm' in onclick or 'forceShow' in onclick or 'quickDemo' in onclick:
        # Sarara lakkoofsa argadhu
        line_no = content[:m.start()].count('\n') + 1
        print(f"   • Sarara {line_no}: {onclick[:80]}...")

# 4. Functions ijoo jiraachuu
print("\n4. Functions ijoo:")
for fn in ['render', 'forceShowDashboard', 'switchAuth', 'quickDemoLogin', 'vDash', 'kpis', 'drawDashChart']:
    exists = f'function {fn}(' in content
    print(f"   • {fn}(): {'✅' if exists else '❌'}")

# 5. JavaScript syntax check (brace balance)
print("\n5. Brace Balance Check:")
script = re.search(r'<script>([\s\S]*?)</script>', content)
if script:
    js = script.group(1)
    opens = js.count('{')
    closes = js.count('}')
    diff = opens - closes
    print(f"   • {{ = {opens}, }} = {closes}, Diff = {diff}")
    if diff != 0:
        print(f"   ⚠️  RAKKOO: Brace balance dogoggora! ({diff:+d})")
        print("      Kun JavaScript syntax error uuma — koodii guutuu ni dhorkaa.")
    else:
        print("   ✅ Brace balance sirrii dha.")

# 6. state.records ramaduu
print("\n6. state.records Assignment (unique):")
assigns = set()
for m in re.finditer(r'state\.records\s*=\s*([^;\n]{0,50})', content):
    assigns.add(m.group(1).strip()[:50])
for a in list(assigns)[:10]:
    print(f"   • {a}")

# 7. Duplicate <script> tags
script_count = content.count('<script')
print(f"\n7. <script> tags: {script_count}")

# 8. Duplicate function definitions
print("\n8. Duplicate functions:")
all_funcs = re.findall(r'function\s+(\w+)\s*\(', content)
from collections import Counter
dups = {k: v for k, v in Counter(all_funcs).items() if v > 1}
if dups:
    for k, v in dups.items():
        print(f"   ⚠️  {k}() — {v} jechuu")
else:
    print("   ✅ Duplicate function hin jiru.")

print("\n" + "=" * 55)
print("📍 Xiinxalli xumurameera.")
print("=" * 55)

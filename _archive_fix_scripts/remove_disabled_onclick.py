import os, re

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    content = f.read()

print("=" * 60)
print("🔧 DISABLED BUTTON ONCLICK HAQUU")
print("=" * 60)

# 1. Button "Current Plan" barbaadi
pattern = re.compile(
    r'<button[^>]*disabled[^>]*>[\s\S]{0,200}?Current Plan[\s\S]{0,30}?</button>',
    re.DOTALL
)

matches = list(pattern.finditer(content))
print(f"\n📍 Button 'Current Plan' disabled argameera: {len(matches)}")

for m in matches:
    line_no = content[:m.start()].count('\n') + 1
    btn_html = m.group(0)
    print(f"\n   Sarara {line_no}:")
    print(f"   {btn_html[:250]}")
    
    # Yoo onclick console.log qaba, sana haqi
    if 'console.log' in btn_html:
        new_btn = re.sub(r'\s*onclick="console\.log\([^)]*\)"', '', btn_html)
        content = content.replace(btn_html, new_btn, 1)
        print(f"   ✅ onclick console.log haqameera")

# 2. Universal: button disabled hunda irraa 'console.log' onclick haqi
pattern2 = re.compile(r'(\<button[^>]*disabled[^>]*)\s*onclick="console\.log\([^"]*\)"')
content, n = pattern2.subn(r'\1', content)
if n > 0:
    print(f"\n✅ Button disabled {n} irraa console.log onclick haqameera")

# 3. Mirkaneessi
with open(html_path, 'w') as f:
    f.write(content)

# Sanada
with open(html_path, 'r') as f:
    new_content = f.read()

# Button disabled onclick check
disabled_with_onclick = 0
for m in re.finditer(r'<button[^>]*disabled[^>]*>', new_content):
    if 'onclick=' in m.group(0):
        disabled_with_onclick += 1

print("\n" + "=" * 60)
print("📍 MIRKANEESSA")
print("=" * 60)
print(f"   Button disabled onclick qabu: {disabled_with_onclick}")

# Buttons onclick hin qabne
without_onclick = 0
submit_count = 0
for m in re.finditer(r'<button\b[^>]*>', new_content):
    tag = m.group(0)
    if 'onclick=' not in tag:
        without_onclick += 1
        if 'type="submit"' in tag:
            submit_count += 1

print(f"   Buttons onclick hin qabne: {without_onclick}")
print(f"   Isaan keessaa type=\"submit\": {submit_count}")
print(f"   Rakkoo guddaan hafe: {without_onclick - submit_count}")

print("\n" + "=" * 60)
print("✅ XUMURAMEERA!")
print("=" * 60)

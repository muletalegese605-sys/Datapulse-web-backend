import os, re

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    content = f.read()

print("=" * 65)
print("🔍 BUTTONS HAFAN - ADDA BAASUU")
print("=" * 65)

# 1. Buttons onclick hin qabne, type=submit MITI
print("\n📋 1. Buttons onclick hin qabne (type=submit MITI):")
count1 = 0
for m in re.finditer(r'<button\b[^>]*>', content):
    tag = m.group(0)
    if 'onclick=' not in tag and 'type="submit"' not in tag:
        count1 += 1
        line_no = content[:m.start()].count('\n') + 1
        end = content.find('</button>', m.end())
        full_btn = content[m.start():end+9] if end > 0 else tag
        text = re.sub(r'<[^>]+>', '', full_btn).strip()[:60]
        id_m = re.search(r'id="([^"]*)"', tag)
        btn_id = id_m.group(1) if id_m else 'NO_ID'
        type_m = re.search(r'type="([^"]*)"', tag)
        btn_type = type_m.group(1) if type_m else 'NO_TYPE'
        print(f"\n   #{count1} Sarara {line_no}:")
        print(f"      ID: {btn_id}")
        print(f"      Type: {btn_type}")
        print(f"      Text: '{text}'")
        print(f"      HTML: {tag[:200]}")

# 2. Buttons disabled onclick qabu
print("\n\n📋 2. Buttons disabled onclick qabu:")
count2 = 0
for m in re.finditer(r'<button[^>]*\bdisabled\b[^>]*>', content):
    tag = m.group(0)
    if 'onclick=' in tag:
        count2 += 1
        line_no = content[:m.start()].count('\n') + 1
        end = content.find('</button>', m.end())
        full_btn = content[m.start():end+9] if end > 0 else tag
        text = re.sub(r'<[^>]+>', '', full_btn).strip()[:60]
        id_m = re.search(r'id="([^"]*)"', tag)
        btn_id = id_m.group(1) if id_m else 'NO_ID'
        onclick_m = re.search(r'onclick="([^"]*)"', tag)
        onclick = onclick_m.group(1) if onclick_m else 'NO_ONCLICK'
        print(f"\n   #{count2} Sarara {line_no}:")
        print(f"      ID: {btn_id}")
        print(f"      Text: '{text}'")
        print(f"      onclick: {onclick[:80]}")
        print(f"      HTML: {tag[:250]}")

if count1 == 0 and count2 == 0:
    print("\n🎉 RAKKOON HUNDI SIRREEEFFAMERA!")
else:
    print(f"\n⚠️  Rakkoo hafe: {count1 + count2}")

print("\n" + "=" * 65)

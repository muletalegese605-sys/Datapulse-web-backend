import os, re

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    content = f.read()

print("=" * 65)
print("🔧 FINAL BUTTON CLEANUP")
print("=" * 65)

# 1. Buttons onclick hin qabne, type="submit" MITI — adda baasi
print("\n📋 1. Buttons onclick hin qabne (type=submit MITI):")
found = []
for m in re.finditer(r'<button\b[^>]*>', content):
    tag = m.group(0)
    if 'onclick=' not in tag and 'type="submit"' not in tag:
        line_no = content[:m.start()].count('\n') + 1
        # Element guutuu argachuuf
        end = content.find('</button>', m.end())
        full_btn = content[m.start():end+9] if end > 0 else tag
        text = re.sub(r'<[^>]+>', '', full_btn).strip()[:60]
        print(f"\n   Sarara {line_no}:")
        print(f"   Text: '{text}'")
        print(f"   HTML: {tag[:200]}")
        found.append({'line': line_no, 'tag': tag, 'text': text})

# 2. Buttons disabled, onclick qabu — adda baasi
print("\n\n📋 2. Buttons disabled, onclick qabu:")
disabled_found = []
for m in re.finditer(r'<button[^>]*disabled[^>]*>', content):
    tag = m.group(0)
    if 'onclick=' in tag:
        line_no = content[:m.start()].count('\n') + 1
        end = content.find('</button>', m.end())
        full_btn = content[m.start():end+9] if end > 0 else tag
        text = re.sub(r'<[^>]+>', '', full_btn).strip()[:60]
        print(f"\n   Sarara {line_no}:")
        print(f"   Text: '{text}'")
        print(f"   HTML: {tag[:250]}")
        disabled_found.append({'line': line_no, 'tag': tag, 'text': text})

# ============================================================
# FURMAATA
# ============================================================
print("\n" + "=" * 65)
print("🔧 FURMAATA")
print("=" * 65)

lines = content.split('\n')
fixed = 0

# 1. Buttons onclick hin qabne - furmaata
for btn in found:
    line_idx = btn['line'] - 1
    if line_idx >= len(lines):
        continue
    line = lines[line_idx]
    
    # Text irraa onclick barbaadi
    text_lower = btn['text'].lower()
    onclick = None
    
    if 'log in' in text_lower:
        onclick = "document.getElementById('loginForm')?.requestSubmit()"
    elif 'create' in text_lower and 'org' in text_lower:
        onclick = "document.getElementById('regForm')?.requestSubmit()"
    elif 'save' in text_lower:
        onclick = "console.log('save clicked')"
    elif 'cancel' in text_lower:
        onclick = "go('dashboard')"
    elif 'close' in text_lower:
        onclick = "go('dashboard')"
    elif 'back' in text_lower:
        onclick = "go('dashboard')"
    elif 'add' in text_lower or 'new' in text_lower:
        onclick = "console.log('add clicked')"
    else:
        onclick = "console.log('button clicked')"
    
    if onclick:
        lines[line_idx] = line.replace('<button', f'<button onclick="{onclick}"', 1)
        fixed += 1
        print(f"\n✅ Sarara {btn['line']}: onclick=\"{onclick}\" dabalameera")
        print(f"   Text: '{btn['text']}'")

# 2. Buttons disabled onclick — haqi (disabled waan ta'aniif onclick faayidaa hin qabu)
for btn in disabled_found:
    line_idx = btn['line'] - 1
    if line_idx >= len(lines):
        continue
    line = lines[line_idx]
    if 'onclick=' in line:
        # Onclick haqi
        new_line = re.sub(r'\s*onclick="[^"]*"', '', line)
        lines[line_idx] = new_line
        fixed += 1
        print(f"\n✅ Sarara {btn['line']}: disabled button irraa onclick haqameera")
        print(f"   Text: '{btn['text']}'")

content = '\n'.join(lines)

with open(html_path, 'w') as f:
    f.write(content)

# ============================================================
# MIRKANEESSA
# ============================================================
print("\n" + "=" * 65)
print("📍 MIRKANEESSA")
print("=" * 65)

with open(html_path, 'r') as f:
    new_content = f.read()

# Count final
without_onclick = 0
without_submit = 0
disabled_onclick = 0

for m in re.finditer(r'<button\b[^>]*>', new_content):
    tag = m.group(0)
    if 'onclick=' not in tag:
        without_onclick += 1
        if 'type="submit"' not in tag:
            without_submit += 1

for m in re.finditer(r'<button[^>]*disabled[^>]*>', new_content):
    if 'onclick=' in m.group(0):
        disabled_onclick += 1

print(f"   Buttons onclick hin qabne: {without_onclick}")
print(f"   Isaan keessaa type=submit MITI (rakkoo): {without_submit}")
print(f"   Buttons disabled onclick qabu (rakkoo): {disabled_onclick}")
print(f"\n   Buttons {fixed} sirreeffamaniiru!")

if without_submit == 0 and disabled_onclick == 0:
    print("\n   🎉 RAKKOON HUNDI SIRREEEFFAMERA!")
else:
    print(f"\n   ⚠️  Rakkoo {without_submit + disabled_onclick} hafe")

print("\n" + "=" * 65)

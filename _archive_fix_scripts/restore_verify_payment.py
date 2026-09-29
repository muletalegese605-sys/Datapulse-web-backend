import os, re

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    content = f.read()

print("=" * 60)
print("🔧 VERIFY & CONFIRM PAYMENT ONCLICK DEEBISUU")
print("=" * 60)

# 1. Verify button — onclick deebisi
pattern_verify = re.compile(
    r'<button\s+type="button"\s+id="verifyBtn"(\s+onclick="[^"]*")?\s+class="w-full py-3 bg-emerald-500',
    re.DOTALL
)

def fix_verify(m):
    tag = m.group(0)
    if 'onclick=' not in tag:
        tag = tag.replace('id="verifyBtn"', 'id="verifyBtn" onclick="verifyEmailCode()"', 1)
    return tag

content, n = pattern_verify.subn(fix_verify, content)
if n > 0:
    print(f"✅ Verify button (sarara 744) onclick deebi'ameera")

# 2. Confirm Payment button — onclick deebisi
pattern_pay = re.compile(
    r'<button\s+type="button"\s+id="payConfirmBtn"(\s+onclick="[^"]*")?\s+class="py-3 bg-emerald-500',
    re.DOTALL
)

def fix_pay(m):
    tag = m.group(0)
    if 'onclick=' not in tag:
        tag = tag.replace('id="payConfirmBtn"', 'id="payConfirmBtn" onclick="confirmPayment()"', 1)
    return tag

content, n = pattern_pay.subn(fix_pay, content)
if n > 0:
    print(f"✅ Confirm Payment button (sarara 888) onclick deebi'ameera")

# 3. Current Plan (3144) — onclick console.log haqi (disabled dha, faayidaa hin qabu)
pattern_current = re.compile(
    r'(<button[^>]*disabled[^>]*)\s*onclick="console\.log\([^)]*\)"([^>]*>Current Plan)',
    re.DOTALL
)
content, n = pattern_current.subn(r'\1\2', content)
if n > 0:
    print(f"✅ Current Plan button (sarara 3144) onclick haqameera")

# ============================================================
# FALLBACK: Yoo patterns sun hin argamne, line-by-line hojjedhu
# ============================================================
lines = content.split('\n')

for i, line in enumerate(lines):
    # Verify button
    if 'id="verifyBtn"' in line and 'onclick=' not in line:
        lines[i] = line.replace('id="verifyBtn"', 'id="verifyBtn" onclick="verifyEmailCode()"', 1)
        print(f"✅ Sarara {i+1}: verifyBtn onclick dabalameera (fallback)")
    
    # Confirm Payment button
    if 'id="payConfirmBtn"' in line and 'onclick=' not in line:
        lines[i] = line.replace('id="payConfirmBtn"', 'id="payConfirmBtn" onclick="confirmPayment()"', 1)
        print(f"✅ Sarara {i+1}: payConfirmBtn onclick dabalameera (fallback)")
    
    # Current Plan — onclick console.log haqi
    if 'Current Plan' in line and 'console.log' in line:
        lines[i] = re.sub(r'\s*onclick="console\.log\([^)]*\)"', '', line)
        print(f"✅ Sarara {i+1}: Current Plan onclick haqameera (fallback)")

content = '\n'.join(lines)

with open(html_path, 'w') as f:
    f.write(content)

# ============================================================
# MIRKANEESSA
# ============================================================
print("\n" + "=" * 60)
print("📍 MIRKANEESSA")
print("=" * 60)

with open(html_path, 'r') as f:
    new_content = f.read()

# Verify button
if 'id="verifyBtn"' in new_content:
    idx = new_content.find('id="verifyBtn"')
    line_no = new_content[:idx].count('\n') + 1
    tag_end = new_content.find('>', idx)
    tag = new_content[new_content.rfind('<button', 0, idx):tag_end+1]
    has_onclick = 'onclick=' in tag
    print(f"   verifyBtn (Sarara {line_no}): {'✅ onclick jira' if has_onclick else '❌ onclick hin jiru'}")

# Confirm Payment
if 'id="payConfirmBtn"' in new_content:
    idx = new_content.find('id="payConfirmBtn"')
    line_no = new_content[:idx].count('\n') + 1
    tag_end = new_content.find('>', idx)
    tag = new_content[new_content.rfind('<button', 0, idx):tag_end+1]
    has_onclick = 'onclick=' in tag
    print(f"   payConfirmBtn (Sarara {line_no}): {'✅ onclick jira' if has_onclick else '❌ onclick hin jiru'}")

# Current Plan
for m in re.finditer(r'<button[^>]*>[\s\S]{0,100}?Current Plan[\s\S]{0,30}?</button>', new_content):
    tag = m.group(0)
    line_no = new_content[:m.start()].count('\n') + 1
    has_onclick = 'onclick=' in tag
    print(f"   Current Plan (Sarara {line_no}): {'⚠️ onclick jira' if has_onclick else '✅ onclick hin jiru (disabled dha)'}")
    break

# Count
without_onclick = 0
without_submit = 0
disabled_with_onclick = 0
for m in re.finditer(r'<button\b[^>]*>', new_content):
    tag = m.group(0)
    if 'onclick=' not in tag:
        without_onclick += 1
        if 'type="submit"' not in tag:
            without_submit += 1

for m in re.finditer(r'<button[^>]*\bdisabled\b[^>]*>', new_content):
    if 'onclick=' in m.group(0):
        disabled_with_onclick += 1

print(f"\n   Buttons onclick hin qabne: {without_onclick}")
print(f"   Isaan keessaa type=submit MITI: {without_submit}")
print(f"   Buttons disabled onclick qabu: {disabled_with_onclick}")

print("\n" + "=" * 60)
print("✅ XUMURAMEERA!")
print("=" * 60)

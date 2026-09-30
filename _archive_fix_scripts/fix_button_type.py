import os, re

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    content = f.read()

print("=" * 60)
print("🔧 BUTTON TYPE FIX")
print("=" * 60)

# 1. Dura mirkaneessi - button kam type qaba, kam hin qabu
print("\n1. Dura (before):")
with_type = len(re.findall(r'<button[^>]*type="', content))
without_type = len(re.findall(r'<button(?![^>]*type=")', content))
print(f"   Button type qabu: {with_type}")
print(f"   Button type hin qabne: {without_type}")

# 2. Button hunda: yoo 'type' hin qabanne, 'type="button"' dabali
# Pattern: <button[^>]*onclick="..."[^>]*>
# Garuu 'type=' hin qabu

def add_type(m):
    tag = m.group(0)
    # Yoo 'type=' hin qabu
    if 'type=' not in tag:
        # <button ...> ta'e, 'type="button"' dabali
        tag = tag.replace('<button', '<button type="button"', 1)
    return tag

# Button hunda barbaadii, type="button" dabali (yoo hin qabu)
content_new = re.sub(r'<button[^>]*>', add_type, content)

# Count how many were modified
changed = content_new != content
content = content_new

# 3. Ammas mirkaneessi
with_type_new = len(re.findall(r'<button[^>]*type="', content))
without_type_new = len(re.findall(r'<button(?![^>]*type=")', content))

print("\n2. Booda (after):")
print(f"   Button type qabu: {with_type_new}")
print(f"   Button type hin qabne: {without_type_new}")

# 4. Button 'Launch App' ilaali
print("\n3. Button 'Launch App':")
for m in re.finditer(r'<button[^>]*>[\s\S]{0,200}?Launch App[\s\S]{0,30}?</button>', content):
    line_no = content[:m.start()].count('\n') + 1
    print(f"   Sarara {line_no}:")
    print(f"   {m.group(0)[:250]}")
    break

# 5. Submit buttons - 'type="submit"' qaban dhiisi
submit_count = len(re.findall(r'<button[^>]*type="submit"', content))
print(f"\n4. Submit buttons (type=\"submit\"): {submit_count}")

with open(html_path, 'w') as f:
    f.write(content)

print("\n" + "=" * 60)
print("✅ BUTTON TYPE FIX XUMURAMEERA!")
print("=" * 60)

# Sanada elements
with open(html_path, 'r') as f:
    new_content = f.read()
print(f"\n📍 Script balance: {len(re.findall(r'<script', new_content))} / {new_content.count('</script>')}")

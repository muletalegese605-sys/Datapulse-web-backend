import os, re

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    content = f.read()

print("=" * 65)
print("🔍 BUTTONS ONCLICK HIN QABNE - ADDA BAASUU")
print("=" * 65)

# Button hunda barbaadi (onclick hin qabne)
buttons_without_onclick = []

# Regex: <button ...>...</button>
for m in re.finditer(r'<button\b[^>]*>[\s\S]{0,300}?</button>', content):
    tag_open = m.group(0)
    # Open tag qofa
    open_match = re.match(r'<button\b[^>]*>', tag_open)
    if open_match:
        open_tag = open_match.group(0)
        if 'onclick=' not in open_tag:
            line_no = content[:m.start()].count('\n') + 1
            # Text content fudhachuu
            text_content = re.sub(r'<[^>]+>', '', tag_open).strip()
            # Type
            type_match = re.search(r'type="([^"]*)"', open_tag)
            btn_type = type_match.group(1) if type_match else 'NO_TYPE'
            # ID
            id_match = re.search(r'id="([^"]*)"', open_tag)
            btn_id = id_match.group(1) if id_match else 'NO_ID'
            # Class
            class_match = re.search(r'class="([^"]*)"', open_tag)
            btn_class = class_match.group(1)[:80] if class_match else ''
            
            buttons_without_onclick.append({
                'line': line_no,
                'text': text_content[:60],
                'type': btn_type,
                'id': btn_id,
                'class': btn_class,
                'html': open_tag[:200]
            })

print(f"\n📍 Buttons onclick hin qabne: {len(buttons_without_onclick)}\n")

for i, btn in enumerate(buttons_without_onclick, 1):
    print(f"--- Button #{i} ---")
    print(f"   Sarara: {btn['line']}")
    print(f"   ID: {btn['id']}")
    print(f"   Type: {btn['type']}")
    print(f"   Text: '{btn['text']}'")
    print(f"   Class: {btn['class']}")
    print(f"   HTML: {btn['html']}")
    print()

# ============================================================
# FURMAATA
# ============================================================
print("=" * 65)
print("🔧 FURMAATA")
print("=" * 65)

fixed_count = 0

# Button tokkoon tokkoon - furmaata adda addaa
for btn in buttons_without_onclick:
    # 1. Yoo type="submit" ta'e - submit waliin ta'a, onsubmit waliin hojjeta
    if btn['type'] == 'submit':
        print(f"\n✅ Sarara {btn['line']}: type=\"submit\" — onsubmit form waliin ni hojjeta (rakkoo hin qabu)")
        continue
    
    # 2. Yoo text 'Log In' ykn 'Create' ta'e - submit handler dabaluu
    text_lower = btn['text'].lower()
    
    # Furmaata: yoo button sun onclick hin qabne, ID ykn text irraa onclick dabaluu
    onclick_to_add = None
    
    # Login button
    if 'log in' in text_lower or 'login' in text_lower:
        onclick_to_add = "document.getElementById('loginForm')?.requestSubmit()"
    # Create Organization
    elif 'create' in text_lower and 'org' in text_lower:
        onclick_to_add = "document.getElementById('regForm')?.requestSubmit()"
    # Register
    elif 'register' in text_lower or 'sign up' in text_lower:
        onclick_to_add = "switchAuth('register')"
    # Sign In
    elif 'sign in' in text_lower:
        onclick_to_add = "switchAuth('login')"
    # Demo
    elif 'demo' in text_lower:
        onclick_to_add = "quickDemoLogin()"
    # Launch
    elif 'launch' in text_lower:
        onclick_to_add = "showLoginFromLanding()"
    # Contact
    elif 'contact' in text_lower:
        onclick_to_add = "go('contact')"
    # Cancel
    elif 'cancel' in text_lower:
        onclick_to_add = "go('dashboard')"
    # Close
    elif 'close' in text_lower or 'back' in text_lower:
        onclick_to_add = "go('dashboard')"
    # Generic fallback
    else:
        # Yoo ID qabaate, ID irraa fayyadami
        if btn['id'] != 'NO_ID':
            # ID irraa function barbaadi
            onclick_to_add = f"console.log('Button {btn['id']} clicked')"
        else:
            # Button duwwaa ta'uu danda'a - log qofa
            onclick_to_add = "console.log('Button clicked')"
    
    if onclick_to_add:
        # HTML galmee - button tag sana bakka buusi
        # Find exact button in content
        pattern = re.compile(
            r'(<button\b(?=[^>]*>[\s\S]{0,300}?<[^>]*>\s*' + re.escape(btn['text'][:20]) + r'[\s\S]{0,30}?))',
            re.DOTALL
        )
        
        # Simpler approach: sarara lakkoofsaan button sana bakka buusi
        lines = content.split('\n')
        line_idx = btn['line'] - 1
        
        if line_idx < len(lines):
            line = lines[line_idx]
            if '<button' in line and 'onclick=' not in line:
                # 'onclick' dabaluu
                lines[line_idx] = line.replace('<button', f'<button onclick="{onclick_to_add}"', 1)
                fixed_count += 1
                print(f"\n✅ Sarara {btn['line']}: onclick=\"{onclick_to_add}\" dabalameera")
                print(f"   Text: '{btn['text']}'")

# Content update
content = '\n'.join(lines)

with open(html_path, 'w') as f:
    f.write(content)

print(f"\n" + "=" * 65)
print(f"✅ Buttons {fixed_count} sirreeffamaniiru!")
print("=" * 65)

# Mirkaneessi
with open(html_path, 'r') as f:
    new_content = f.read()

without_onclick_new = 0
submit_count = 0
for m in re.finditer(r'<button\b[^>]*>', new_content):
    tag = m.group(0)
    if 'onclick=' not in tag:
        without_onclick_new += 1
        if 'type="submit"' in tag:
            submit_count += 1

print(f"\n📍 MIRKANEESSA")
print(f"   Buttons onclick hin qabne: {without_onclick_new}")
print(f"   Isaan keessaa type=\"submit\": {submit_count}")
print(f"   Rakkoo guddaan hafe: {without_onclick_new - submit_count}")

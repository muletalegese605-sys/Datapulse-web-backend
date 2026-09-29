import os, re

html_path = os.path.expanduser('~/datapulse-web/public/index.html')
backup_path = os.path.expanduser('~/datapulse-web/public/index.html.bak_mock')

with open(html_path, 'r') as f:
    current = f.read()

with open(backup_path, 'r') as f:
    backup = f.read()

print("=" * 55)
print("🔧 RESTORE LOGIN FROM BACKUP")
print("=" * 55)

# 1. Backup irraa #loginScreen HTML kutaa fudhachiisi
# #loginScreen jalqabee, </div> dhuma isaa barbaadi
def extract_el(content, el_id):
    m = re.search(r'<div[^>]*id="' + el_id + r'"[^>]*>', content)
    if not m:
        return None
    start = m.start()
    # Div guutuu barbaadi - nesting count
    depth = 0
    i = m.end() - 1
    while i < len(content):
        if content[i:i+4] == '<div':
            depth += 1
        elif content[i:i+6] == '</div>':
            if depth == 0:
                return content[start:i+6]
            depth -= 1
        i += 1
    return None

backup_login = extract_el(backup, 'loginScreen')
backup_landing = extract_el(backup, 'landingPage')
backup_app = extract_el(backup, 'app')

print(f"\n1. Backup irraa kutaa:")
print(f"   #loginScreen: {'✅' if backup_login else '❌'} ({len(backup_login) if backup_login else 0} chars)")
print(f"   #landingPage: {'✅' if backup_landing else '❌'} ({len(backup_landing) if backup_landing else 0} chars)")
print(f"   #app: {'✅' if backup_app else '❌'} ({len(backup_app) if backup_app else 0} chars)")

# 2. File ammaa keessaa #loginScreen balleeffame sana bakka buusi
current_login = extract_el(current, 'loginScreen')
print(f"\n2. File ammaa keessaa:")
print(f"   #loginScreen: {'✅' if current_login else '❌'} ({len(current_login) if current_login else 0} chars)")

if backup_login and current_login:
    current = current.replace(current_login, backup_login)
    print(f"\n   ✅ #loginScreen backup irraa deebi'ameera")
elif backup_login and not current_login:
    # Yoo ammaa keessaa dhabame, landingPage dura galchi
    m = re.search(r'<div[^>]*id="landingPage"[^>]*>', current)
    if m:
        current = current[:m.start()] + backup_login + '\n' + current[m.start():]
        print(f"\n   ✅ #loginScreen dabalameera (landingPage dura)")

# 3. #app fi #main mirkaneessi
current_app = extract_el(current, 'app')
print(f"\n3. #app ammaa keessa:")
print(f"   #app: {'✅' if current_app else '❌'}")

with open(html_path, 'w') as f:
    f.write(current)

print("\n" + "=" * 55)
print("✅ RESTORE xumurameera!")
print("=" * 55)

# Deploy booda mirkaneessi

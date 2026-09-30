import os, re

html_path = os.path.expanduser('~/datapulse-web/public/index.html')
backup_path = os.path.expanduser('~/datapulse-web/public/index.html.bak_mock')

with open(html_path, 'r') as f:
    current = f.read()

with open(backup_path, 'r') as f:
    backup = f.read()

# extract_el function - closing div sirriitti dubbisuuf
def extract_el(content, el_id):
    # Element karaa div, main, section, kkf barbaadi
    m = re.search(r'<(div|main|section|article)[^>]*id="' + el_id + r'"[^>]*>', content)
    if not m:
        return None, None
    tag_name = m.group(1)
    start = m.start()
    # Nesting count fayyadami
    depth = 0
    i = m.end() - 1
    open_pat = '<' + tag_name
    close_pat = '</' + tag_name + '>'
    while i < len(content):
        if content[i:i+len(open_pat)] == open_pat and content[i+len(open_pat)] in ' \t\n>':
            depth += 1
        elif content[i:i+len(close_pat)] == close_pat:
            if depth == 0:
                return content[start:i+len(close_pat)], tag_name
            depth -= 1
            i += len(close_pat) - 1
        i += 1
    return None, None

# 1. #app element ammaa fi backup keessaa ilaali
current_app, current_tag = extract_el(current, 'app')
backup_app, backup_tag = extract_el(backup, 'app')

print(f"1. #app Element:")
print(f"   Backup: <{backup_tag}> ({len(backup_app) if backup_app else 0} chars)")
print(f"   Current: <{current_tag}> ({len(current_app) if current_app else 0} chars)")

if backup_app and not current_app:
    # #app dhabameera - landingPage dura galchi
    m = re.search(r'<div[^>]*id="landingPage"[^>]*>', current)
    if m:
        current = current[:m.start()] + backup_app + '\n' + current[m.start():]
        print(f"\n   ✅ #app backup irraa dabalameera")
elif backup_app and current_app:
    # Lamaanuu jiru - backup isa guddaa ta'e bakka buusi (yoo guddaan jiraate)
    if len(backup_app) > len(current_app) * 2:
        current = current.replace(current_app, backup_app)
        print(f"\n   ✅ #app backup waliin bakka bu'ameera")
    else:
        print(f"\n   ✅ #app ammaa jira, rakkoo hin qabu")
elif not backup_app:
    print(f"\n   ⚠️  Backup keessaa #app hin argamne!")

# 2. #main element mirkaneessi
current_main, _ = extract_el(current, 'main')
if current_main:
    print(f"\n2. #main Element: ✅ ({len(current_main)} chars)")
else:
    print(f"\n2. #main Element: ❌ Dhabameera!")

# 3. Critical elements hunda
print(f"\n3. Critical Elements:")
for eid in ['landingPage', 'loginScreen', 'app', 'main', 'tbLogin', 'tbRegister']:
    el, tag = extract_el(current, eid)
    status = '✅' if el else '❌'
    print(f"   {status} #{eid}")

with open(html_path, 'w') as f:
    f.write(current)

print("\n" + "=" * 55)
print("✅ RESTORE APP xumurameera!")
print("=" * 55)

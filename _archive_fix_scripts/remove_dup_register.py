import os, re

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    content = f.read()

# Button tbRegister isa duwwaa (barruu hin qabne) haqi
# Fakkeenya: <button id="tbRegister" onclick="switchAuth(\'register\')"></button>
pattern = re.compile(
    r'\s*<button\s+id="tbRegister"[^>]*>\s*</button>',
    re.IGNORECASE
)

matches = pattern.findall(content)
if matches:
    content = pattern.sub('', content)
    print(f"✅ Button tbRegister duwwaa {len(matches)} haqameera!")
else:
    print("⚠️ Button duwwaa hin argamne.")

# Yoo lamaan jiraatan, kan barruu qabu qofa dhiisi
count = content.count('id="tbRegister"')
if count > 1:
    print(f"⚠️ Button tbRegister {count} jira. Mirkaneessi:")
    for m in re.finditer(r'<button[^>]*id="tbRegister"[^>]*>[^<]*</button>', content):
        print(f"   - {m.group(0)[:120]}")

with open(html_path, 'w') as f:
    f.write(content)

print("📍 Hojii xumurameera!")

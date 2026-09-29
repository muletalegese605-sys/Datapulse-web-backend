import os, re

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    content = f.read()

# Balance tracking - char by char
balance = 0
result = []
i = 0
inserts_middle = 0

while i < len(content):
    if content[i:i+9] == '</script>':
        result.append('</script>')
        if balance > 0:
            balance -= 1
        i += 9
    elif content[i:i+7] == '<script':
        end = content.find('>', i)
        if end == -1:
            result.append(content[i])
            i += 1
            continue
        tag = content[i:end+1]
        # Yoo script banaa jira, sana dura </script> galchi
        if balance > 0:
            result.append('\n</script>\n')
            balance = 0
            inserts_middle += 1
        result.append(tag)
        balance += 1
        i = end + 1
    else:
        result.append(content[i])
        i += 1

content = ''.join(result)

# Yoo ammas balance > 0 ta'e, </body> dura </script> dabali
if balance > 0:
    if '</body>' in content:
        content = content.replace('</body>', ('</script>\n' * balance) + '</body>', 1)
        print(f"✅ {balance} </script> before </body> dabalameera")
    else:
        content += ('</script>\n' * balance)

with open(html_path, 'w') as f:
    f.write(content)

# Mirkaneessi
opens = len(re.findall(r'<script\b[^>]*>', content))
closes = len(re.findall(r'</script>', content))
print("=" * 50)
print(f"✅ Opens: {opens}, Closes: {closes}, Diff: {opens - closes}")
print(f"📍 Inserts gidduu: {inserts_middle}")
print("=" * 50)

# Sanada orphaned code check
orphan_count = 0
for m in re.finditer(r'function startTicker\(\)|setInterval\(\(\)\s*=>|Array\.from\(bars\.children\)', content):
    line_no = content[:m.start()].count('\n') + 1
    before = content[max(0, m.start()-800):m.start()]
    # Yoo script tag keessaa bahuu baate
    if before.rfind('<script') < before.rfind('</script>'):
        print(f"⚠️  Sarara {line_no}: Ammas orphaned!")
        orphan_count += 1
if orphan_count == 0:
    print("✅ Orphaned code hundi sirreeffameera!")

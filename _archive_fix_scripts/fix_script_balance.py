import os

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")

# 1. Sarara 20 (index 19) - </script> haqi (yoo sana irratti ta'e)
# Sarara jalqabaa fi dhumaa mirkaneessi
for check_line in [19, 20, 21]:
    if check_line < len(lines):
        print(f"Line {check_line+1}: {repr(lines[check_line].rstrip())[:100]}")

print("=" * 50)

# 2. Sarara 20 (index 19) irraa </script> haqi
# Garuu, akka sirriitti, dura script tag #2 fi #3 eessa akka jiran ilaali
opens = []
closes = []
for i, line in enumerate(lines):
    for _ in range(line.count('<script')):
        # '<script' kan 'src' qabu adda baasi
        if '<script' in line:
            opens.append(i)
    for _ in range(line.count('</script>')):
        closes.append(i)

print(f"Script opens (sarara): {[o+1 for o in opens]}")
print(f"Script closes (sarara): {[c+1 for c in closes]}")

# 3. Kan lammaffaan script open (index 1) - line 11
# Kan lammaffaan script close (index 1) - line 20
# Kanaaf, kan sadaffaan close (index 2) sun line 3467 ta'uu qaba
# Garuu, kan lammaffaan close sun line 20 irratti jira - DOGOGGORA

# Furmaata: Kan lammaffaan close (line 20) haqi
if len(closes) >= 2:
    line_to_remove = closes[1]  # Line 20 (0-index 19)
    print(f"\n🗑️  Sarara {line_to_remove + 1} irraa </script> haquu...")
    # Kun sarara dursee cufee jira
    content = lines[line_to_remove]
    # Yoo sararri kun </script> qofa qabate, sarara guutuu haqi
    if content.strip() == '</script>':
        del lines[line_to_remove]
        print(f"✅ Sarara {line_to_remove + 1} haqameera (</script> qofa ture)")
    else:
        # Yoo content biraa waliin jira, </script> qofa haqi
        new_content = content.replace('</script>', '', 1)
        lines[line_to_remove] = new_content
        print(f"✅ Sarara {line_to_remove + 1} irraa </script> haqameera")

# 4. Ammas: kan sadaffaan script open (line 819) - kunis dogoggora
# Sababni: script #2 sun line 11 irraa jalqabee, line 3467 irratti cufamuu qaba
# Kanaaf, script open lammaffaan (line 819) haquu qabna
# Amma indices jijjiiramanii jiru, kanaaf ammas barbaadi
opens = [i for i, line in enumerate(lines) if '<script' in line and 'src=' not in line]
print(f"\nAmma script opens (inline): {[o+1 for o in opens]}")

if len(opens) >= 2:
    # Kan lammaffaan inline open (line 819 ture)
    line_to_remove = opens[1]
    content = lines[line_to_remove]
    if content.strip() == '<script>':
        del lines[line_to_remove]
        print(f"✅ Sarara {line_to_remove + 1} haqameera (<script> qofa ture)")
    else:
        new_content = content.replace('<script>', '', 1)
        lines[line_to_remove] = new_content
        print(f"✅ Sarara {line_to_remove + 1} irraa <script> haqameera")

# 5. Dhuma irratti, </body> dura </script> mirkaneessi
opens_count = sum(1 for line in lines if '<script' in line and 'src=' not in line)
closes_count = sum(1 for line in lines if '</script>' in line)
print(f"\n📍 Balance check: {opens_count} opens, {closes_count} closes")

if opens_count > closes_count:
    diff = opens_count - closes_count
    for i in range(len(lines) - 1, -1, -1):
        if '</body>' in lines[i]:
            lines.insert(i, '</script>\n' * diff)
            print(f"✅ {diff} </script> before </body> dabalameera")
            break

with open(html_path, 'w') as f:
    f.writelines(lines)

print("\n" + "=" * 50)
print("✅ SCRIPT BALANCE FIX xumurameera!")
print("=" * 50)

# Mirkaneessi
with open(html_path, 'r') as f:
    content = f.read()
print(f"Final opens: {content.count('<script') - content.count('<script src')}")
print(f"Final closes: {content.count('</script>')}")

# Function render check - sarara mirkaneessi
idx = content.find('function render(')
if idx > 0:
    line_no = content[:idx].count('\n') + 1
    print(f"\nfunction render() sarara {line_no} irratti argameera")
    # Kun script tag keessa jira?
    before = content[max(0, idx-5000):idx]
    last_open = before.rfind('<script')
    last_close = before.rfind('</script>')
    in_script = last_open > last_close
    print(f"   Script keessa: {'✅ EEYY' if in_script else '❌ LAKKI'}")

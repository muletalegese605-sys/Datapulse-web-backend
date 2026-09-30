import os, re

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    content = f.read()

print("=" * 55)
print("🔧 KILL LAST ORPHAN")
print("=" * 55)

# 1. Kanneen 'Yeroo login/demo tuqtui' jalqabee, '})' xumuran hunda haqi
pattern = r'\n?\s*// Yeroo login/demo tuqtui[\s\S]*?(?=\n\s*//\s*=+|\n\s*<script|\n\s*</body>|\n\s*</html>|$)'
new_content, n = re.subn(pattern, '', content, count=5, flags=re.DOTALL)
if n > 0:
    content = new_content
    print(f"  🗑️  'Yeroo login/demo tuqtui' block {n} haqameera")

# 2. Kanneen 'document.addEventListener' jalqabanii, 'forceRender' ykn 'bootstrap' qaban, '})' xumuran haqi
lines = content.split('\n')
new_lines = []
in_orphan = False
orphan_count = 0
for line in lines:
    stripped = line.strip()
    # Yoo sararri '// Yeroo' ykn 'document.addEventListener' jalqabee, 'forceRender'/'quick demo' qabaate, orphan jalqabi
    if ('// Yeroo' in stripped and ('forceRender' in stripped or 'login' in stripped.lower())) or \
       ('document.addEventListener' in stripped and ('quick demo' in stripped.lower() or 'forceRender' in stripped)):
        in_orphan = True
        orphan_count += 1
        continue
    # Yoo orphan keessa jirru, hamma '}' qofa ta'e xumuratti haqi
    if in_orphan:
        orphan_count += 1
        if stripped == '}' or stripped == '});' or stripped == '})();' or stripped.endswith('}); //'):
            in_orphan = False
        continue
    new_lines.append(line)

if orphan_count > 0:
    content = '\n'.join(new_lines)
    print(f"  🗑️  Orphan lines {orphan_count} haqamaniiru")

# 3. Yoo ammas code text ta'ee jiraate (forceRender mentions), hunda haqi
if 'forceRender' in content:
    # forceRender jedhu bakka hundaa haqi
    content = re.sub(r'\bforceRender\b', '/* removed */', content)
    print(f"  🗑️  forceRender mentions hunda haqamaniiru")

# 4. Script tags madaallii
opens = len(re.findall(r'<script\b[^>]*>', content))
closes = content.count('</script>')
diff = opens - closes
print(f"\nScript balance: {opens} opens, {closes} closes, Diff = {diff}")

if diff > 0:
    if '</body>' in content:
        content = content.replace('</body>', ('\n</script>\n' * diff) + '</body>', 1)
        print(f"  ✅ {diff} </script> before </body> dabalameera")
elif diff < 0:
    excess = -diff
    idxs = [m.start() for m in re.finditer(r'</script>', content)]
    for idx in reversed(idxs[1:]):
        content = content[:idx] + content[idx+9:]
        excess -= 1
        if excess == 0:
            break
    print(f"  ✅ </script> {-diff} haqameera")

# 5. Sanada: orphan code (text ta'ee mul'atu) jiraachuu fi dhabuu
# Kanneen 'setInterval', 'addEventListener' fi '<script>' ala jiran
orphan_patterns = [
    r'document\.addEventListener\([^)]*,\s*function\([^)]*\)\s*\{[^}]*forceRender',
    r'// Yeroo login/demo',
    r'/\* removed \*/',
]
for pat in orphan_patterns:
    matches = re.findall(pat, content)
    if matches:
        print(f"  ⚠️  Orphan pattern {len(matches)} ammas jira: {pat[:40]}")

with open(html_path, 'w') as f:
    f.write(content)

# Mirkaneessi
with open(html_path, 'r') as f:
    content = f.read()

print("\n" + "=" * 55)
print("📍 MIRKANEESSA")
print("=" * 55)
print(f"<script> tags: {len(re.findall(r'<script\b[^>]*>', content))}")
print(f"</script> tags: {content.count('</script>')}")
print(f"forceRender mentions: {content.count('forceRender')}")
print(f"function render() jira: {'✅' if 'function render(' in content else '❌'}")

# function render() script keessa?
idx = content.find('function render(')
if idx > 0:
    before = content[max(0, idx-5000):idx]
    last_open = before.rfind('<script')
    last_close = before.rfind('</script>')
    in_script = last_open > last_close
    print(f"function render() script keessa: {'✅' if in_script else '❌'}")
    # Yoo ala jira, bakka ilaali
    if not in_script:
        line_no = content[:idx].count('\n') + 1
        print(f"   function render() sarara {line_no} irratti jira — kun SCRIPT ALAAAA")
        # Script tag isa dhumaa duraa fi booda agarsiisi
        print(f"   Script tag isa dhumaa: sarara {before[:last_open].count(chr(10))+1}")
        print(f"   </script> isa dhumaa: sarara {before[:last_close].count(chr(10))+1}")

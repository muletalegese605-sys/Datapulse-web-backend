import os, re

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    content = f.read()

print("=" * 55)
print("🔧 FINAL CLEANUP")
print("=" * 55)

# 1. forceRender orphan blocks hunda haqi
# Kanneen 'forceRender' jalqabanii, '})();' xumuran
patterns = [
    r'\n?\s*//\s*=+\s*NUCLEAR DASHBOARD FIX[\s\S]*?(?=\n\s*//\s*=+\s*FINAL|\n\s*<script|\n\s*</body>|$)',
    r'\n?\s*//\s*=+\s*FINAL DASHBOARD RENDER[\s\S]*?(?=\n\s*//\s*=+|\n\s*<script|\n\s*</body>|$)',
    r'\n?\s*//\s*=+\s*APP VISIBILITY FIX[\s\S]*?(?=\n\s*//\s*=+|\n\s*<script|\n\s*</body>|$)',
    r'\n?\s*//\s*=+\s*DASHBOARD SHOW FIX[\s\S]*?(?=\n\s*//\s*=+|\n\s*<script|\n\s*</body>|$)',
    r'\n?\s*//\s*=+\s*AUTH BACKUP HANDLER[\s\S]*?(?=\n\s*//\s*=+|\n\s*<script|\n\s*</body>|$)',
    r'\n?\s*//\s*=+\s*BACKEND FIRST LOADER[\s\S]*?(?=\n\s*//\s*=+|\n\s*<script|\n\s*</body>|$)',
    r'\n?\s*//\s*=+\s*STATE GUARD[\s\S]*?(?=\n\s*//\s*=+|\n\s*<script|\n\s*</body>|$)',
    r'\n?\s*//\s*=+\s*FORCE RENDER CONTENT[\s\S]*?(?=\n\s*//\s*=+|\n\s*<script|\n\s*</body>|$)',
]

for pat in patterns:
    content, n = re.subn(pat, '', content, count=1, flags=re.DOTALL)
    if n > 0:
        print(f"  🗑️  Kutaa haqameera")

# 2. Amma 'forceRender' lamaan hafe, hunda haqi
while 'forceRender' in content:
    idx = content.find('forceRender')
    if idx == -1: break
    
    # Sararri jalqabaa fi xumuraa barbaadi
    line_start = content.rfind('\n', 0, idx) + 1
    line_no = content[:idx].count('\n') + 1
    
    # Xumura: '})();' ykn '});' ykn '</script>' barbaadi
    end = content.find('})();', idx)
    if end == -1:
        end = content.find('});', idx)
    if end == -1:
        break
    end += 5
    
    # Sarara guutuu haqi
    removed_chunk = content[line_start:end]
    content = content[:line_start] + content[end:]
    print(f"  🗑️  Sarara {line_no} forceRender haqameera")

# 3. Script tags madaallii
opens = len(re.findall(r'<script\b[^>]*>', content))
closes = content.count('</script>')
diff = opens - closes

print(f"\nScript balance: {opens} opens, {closes} closes, Diff = {diff}")

# Yoo opens > closes, </body> dura </script> dabali
if diff > 0:
    if '</body>' in content:
        content = content.replace('</body>', ('\n</script>\n' * diff) + '</body>', 1)
        print(f"  ✅ {diff} </script> before </body> dabalameera")
elif diff < 0:
    # Yoo closes > opens, </script> tokko haqi - inni jalqabaa (kan tailwind) dhiisi
    excess = -diff
    # Bakka lammaffaa </script> haqi
    idxs = [m.start() for m in re.finditer(r'</script>', content)]
    for idx in reversed(idxs[1:]):
        content = content[:idx] + content[idx+9:]
        excess -= 1
        if excess == 0:
            break
    print(f"  ✅ </script> {-diff} haqameera")

# 4. Final check
opens = len(re.findall(r'<script\b[^>]*>', content))
closes = content.count('</script>')
print(f"\nFinal: {opens} opens, {closes} closes")

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

# render() script keessa jira?
idx = content.find('function render(')
if idx > 0:
    before = content[max(0, idx-2000):idx]
    # Script tag isa dhumaa barbaadi
    last_open = before.rfind('<script')
    last_close = before.rfind('</script>')
    in_script = last_open > last_close
    print(f"function render() script keessa: {'✅' if in_script else '❌'}")

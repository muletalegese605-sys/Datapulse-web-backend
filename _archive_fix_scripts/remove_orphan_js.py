import os, re

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    content = f.read()

print("=" * 55)
print("🔍 ORPHANED JS REMOVAL")
print("=" * 55)

# 1. Kutaa 'NUCLEAR DASHBOARD FIX' fi 'FINAL DASHBOARD RENDER' haqi
# Kanneen kunneen text ta'anii mul'atan - script tag ala waan jiraniif
patterns_to_remove = [
    # NUCLEAR DASHBOARD FIX kutaa
    r'\n?\s*//\s*=+\s*NUCLEAR DASHBOARD FIX\s*=+[\s\S]*?(?=\n\s*//\s*=+\s*FINAL DASHBOARD RENDER|\n\s*<script|\n\s*</body>|\n\s*</html>|$)',
    # FINAL DASHBOARD RENDER kutaa
    r'\n?\s*//\s*=+\s*FINAL DASHBOARD RENDER\s*=+[\s\S]*?(?=\n\s*//\s*=+|\n\s*<script|\n\s*</body>|\n\s*</html>|$)',
    # APP VISIBILITY FIX
    r'\n?\s*//\s*=+\s*APP VISIBILITY FIX\s*=+[\s\S]*?(?=\n\s*//\s*=+|\n\s*<script|\n\s*</body>|\n\s*</html>|$)',
    # FORCE RENDER CONTENT
    r'\n?\s*//\s*=+\s*FORCE RENDER CONTENT\s*=+[\s\S]*?(?=\n\s*//\s*=+|\n\s*<script|\n\s*</body>|\n\s*</html>|$)',
    # STATE GUARD
    r'\n?\s*//\s*=+\s*STATE GUARD\s*=+[\s\S]*?(?=\n\s*//\s*=+|\n\s*<script|\n\s*</body>|\n\s*</html>|$)',
    # DASHBOARD SHOW FIX
    r'\n?\s*//\s*=+\s*DASHBOARD SHOW FIX\s*=+[\s\S]*?(?=\n\s*//\s*=+|\n\s*<script|\n\s*</body>|\n\s*</html>|$)',
    # AUTH BACKUP HANDLER
    r'\n?\s*//\s*=+\s*AUTH BACKUP HANDLER\s*=+[\s\S]*?(?=\n\s*//\s*=+|\n\s*<script|\n\s*</body>|\n\s*</html>|$)',
    # BACKEND FIRST LOADER
    r'\n?\s*//\s*=+\s*BACKEND FIRST LOADER\s*=+[\s\S]*?(?=\n\s*//\s*=+|\n\s*<script|\n\s*</body>|\n\s*</html>|$)',
    # DASHBOARD RENDER BOOST
    r'\n?\s*//\s*=+\s*DASHBOARD RENDER BOOST\s*=+[\s\S]*?(?=\n\s*//\s*=+|\n\s*<script|\n\s*</body>|\n\s*</html>|$)',
    # VISIBLE DIAGNOSTIC OVERLAY
    r'\n?\s*//\s*=+\s*VISIBLE DIAGNOSTIC OVERLAY\s*=+[\s\S]*?(?=\n\s*//\s*=+|\n\s*<script|\n\s*</body>|\n\s*</html>|$)',
    # UNIVERSAL BUTTON HANDLER
    r'\n?\s*//\s*=+\s*UNIVERSAL BUTTON HANDLER\s*=+[\s\S]*?(?=\n\s*//\s*=+|\n\s*<script|\n\s*</body>|\n\s*</html>|$)',
    # LAUNCH BUTTON BACKUP
    r'\n?\s*//\s*=+\s*LAUNCH BUTTON BACKUP\s*=+[\s\S]*?(?=\n\s*//\s*=+|\n\s*<script|\n\s*</body>|\n\s*</html>|$)',
    # CLEAN BOOTSTRAP
    r'\n?\s*//\s*=+\s*CLEAN BOOTSTRAP\s*=+[\s\S]*?(?=\n\s*//\s*=+|\n\s*<script|\n\s*</body>|\n\s*</html>|$)',
    # BACKEND API INTEGRATION
    r'\n?\s*//\s*=+\s*BACKEND API INTEGRATION\s*=+[\s\S]*?(?=\n\s*//\s*=+|\n\s*<script|\n\s*</body>|\n\s*</html>|$)',
]

total_removed = 0
for pat in patterns_to_remove:
    new_content, n = re.subn(pat, '', content, count=1, flags=re.DOTALL)
    if n > 0:
        content = new_content
        total_removed += 1
        # Tag name print
        tag_match = re.search(r'//\s*=+\s*([A-Z][A-Z\s]+?)\s*=+', pat)
        if tag_match:
            print(f"  🗑️  {tag_match.group(1)} haqameera")

print(f"\n✅ Kutaa {total_removed} haqamaniiru!")

# 2. Yoo ammas 'forceRender' text ta'ee jiraate, sana haqi
# Kun sarara 'window.addEventListener' jalqabee, '});' xumuru dha
if 'forceRender' in content:
    # Kanneen 'forceRender' qaban hunda adda baasi
    lines = content.split('\n')
    new_lines = []
    in_orphan_block = False
    skip_count = 0
    for line in lines:
        stripped = line.strip()
        # Yoo sararri 'window.addEventListener(' jalqabee, 'forceRender' qabaate, orphan block jalqabi
        if 'window.addEventListener' in stripped and 'forceRender' in content[content.find(line):content.find(line)+500]:
            in_orphan_block = True
            skip_count += 1
            continue
        # Yoo orphan block keessa jirru, hamma '});' ykn '})();' xumuratti haqi
        if in_orphan_block:
            skip_count += 1
            if stripped.endswith('});') or stripped.endswith('})();') or stripped.endswith('}); //'):
                in_orphan_block = False
            continue
        new_lines.append(line)
    if skip_count > 0:
        content = '\n'.join(new_lines)
        print(f"  🗑️  Orphan block {skip_count} sarara haqameera")

with open(html_path, 'w') as f:
    f.write(content)

# 3. Mirkaneessi
with open(html_path, 'r') as f:
    content = f.read()

print("\n" + "=" * 55)
print("📍 MIRKANEESSA")
print("=" * 55)
print(f"<script> tags: {len(re.findall(r'<script\b[^>]*>', content))}")
print(f"</script> tags: {content.count('</script>')}")
print(f"forceRender mentions: {content.count('forceRender')}")
print(f"function render() jira: {'✅' if 'function render(' in content else '❌'}")


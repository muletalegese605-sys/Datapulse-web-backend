import os, re

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    content = f.read()

print("=" * 55)
print("🔍 SCRIPT TAG ANALYSIS")
print("=" * 55)

# 1. <script> fi </script> lakkoofsa
opens = len(re.findall(r'<script\b[^>]*>', content))
closes = len(re.findall(r'</script>', content))
print(f"\n1. <script> tags: {opens}")
print(f"   </script> tags: {closes}")
print(f"   Diff: {opens - closes}")

# 2. Kanneen 'src' hin qaban (inline scripts)
inline = re.findall(r'<script\b(?![^>]*\bsrc=)[^>]*>', content)
print(f"\n2. Inline <script> tags (src malee): {len(inline)}")

# 3. Yoo opens != closes ta'e, furmaata
if opens != closes:
    print("\n⚠️  RAKKOO: Script tag balance dogoggora!")
    print("   Sababni: '</script>' tokko haqameera ykn '<script>' tokko hin cufamne.")
    
    # Furmaata: Yoo opens > closes ta'e, </script> dabalii
    # Yoo opens < closes ta'e, <script> dabalii
    if opens > closes:
        # Bakka 'text ta'ee mul'atu' jiru barbaadii, </script> dabaluu
        # Kun yeroo baay'ee 'function startTicker' ykn 'setInterval' booda argama
        diff = opens - closes
        print(f"\n   Furmaata: </script> {diff} dabalii...")
        
        # Bakka 'setInterval' fi 'function startTicker' jalqabee code sun jiru barbaadi
        # Sanatti, </script> ni daballa - code sana </script> dura galchuuf
        
        # Sarara lakkoofsaan: script open tags hunda ibsi
        print("\n   Script tags:")
        for i, m in enumerate(re.finditer(r'<script\b[^>]*>', content)):
            line_no = content[:m.start()].count('\n') + 1
            print(f"   #{i+1} Sarara {line_no}: {m.group(0)[:80]}")
    
    print("\n   ⚠️  Mala salphaa: 'body' element keessatti script hunda galchi.")

# 4. Script tag kanneen adda addaa fi bifa isaanii
print("\n3. Script Tags Detail:")
for i, m in enumerate(re.finditer(r'<script\b[^>]*>', content)):
    line_no = content[:m.start()].count('\n') + 1
    tag = m.group(0)
    # Tag sun gabaabaa ta'uu qaba. Yoo dheeraa ta'e, dogoggora
    if len(tag) > 100:
        print(f"   ⚠️  Sarara {line_no}: Tag dheeraa ({len(tag)} chars) — broken!")
        print(f"      {tag[:80]}...")
    else:
        print(f"   ✅ Sarara {line_no}: {tag}")

# 5. Kutaa 'text ta'ee mul'atu' (orphaned JS) barbaadi
# Kanneen 'function startTicker' ykn 'setInterval' fi '<script>' ala jiran
print("\n4. Orphaned JS Code (text ta'ee mul'atu):")
orphan_patterns = [
    r'function startTicker\(\)',
    r'setInterval\(\(\)\s*=>',
    r'Array\.from\(bars\.children\)',
]
for pat in orphan_patterns:
    for m in re.finditer(pat, content):
        line_no = content[:m.start()].count('\n') + 1
        # Sanatti, script tag kunniin keessa jiraachuu fi dhabuu ilaali
        # Dursaa 500 chars keessaa '<script>' barbaadi
        before = content[max(0, m.start()-500):m.start()]
        if '<script' not in before or '</script>' in before:
            print(f"   ⚠️  Sarara {line_no}: {pat} — SCRIPT TAG ALAAAA!")
        else:
            print(f"   ✅ Sarara {line_no}: {pat} — script keessa")

# 6. Script Tags lamaan walitti fufanii?
print("\n5. Duplicate <script></script> tags:")
for m in re.finditer(r'<script\b[^>]*>\s*</script>', content):
    line_no = content[:m.start()].count('\n') + 1
    print(f"   • Sarara {line_no}: <script></script> duwwaa")

print("\n" + "=" * 55)
print("📍 Xiinxalli xumurameera.")
print("=" * 55)

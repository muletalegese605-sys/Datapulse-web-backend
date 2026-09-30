import os, re

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    content = f.read()

print("=" * 55)
print("🔍 SCRIPT STRUCTURE ANALYSIS")
print("=" * 55)

# 1. Script tags hunda - sarara lakkoofsaan
print("\n1. Script Tags (jiraachuu fi bakka):")
for i, m in enumerate(re.finditer(r'<script\b[^>]*>', content)):
    line_no = content[:m.start()].count('\n') + 1
    print(f"   OPEN #{i+1}: Sarara {line_no}")
for i, m in enumerate(re.finditer(r'</script>', content)):
    line_no = content[:m.start()].count('\n') + 1
    print(f"   CLOSE #{i+1}: Sarara {line_no}")

# 2. function render() bakka jiru
print("\n2. Functions bakka jiran:")
for fn in ['render', 'vDash', 'kpis', 'DP.api']:
    for m in re.finditer(re.escape(fn), content):
        line_no = content[:m.start()].count('\n') + 1
        # 200 chars dura ilaali - script keessa jira?
        before = content[max(0, m.start()-3000):m.start()]
        last_open = before.rfind('<script')
        last_close = before.rfind('</script>')
        in_script = last_open > last_close
        status = '✅ script keessa' if in_script else '❌ SCRIPT ALAAAA'
        print(f"   {fn} (Sarara {line_no}): {status}")
        break

# 3. Syntax error check - specific area
print("\n3. Critical Area Check:")
# Bakka <script> tag jalqabee, function render() jiru
m = re.search(r'<script\b[^>]*>\s*(?://[^\n]*\n\s*)*function\s+render', content)
if m:
    print(f"   ✅ function render() script tag jalqabaa keessa jira")
else:
    print(f"   ❌ function render() script tag jalqabaa keessaa hin jiru!")
    # Bakka jiru ilaali
    m2 = re.search(r'function\s+render\s*\(', content)
    if m2:
        line_no = content[:m2.start()].count('\n') + 1
        print(f"   function render() sarara {line_no} irratti argameera")
        # Dursaa 500 chars agarsiisi
        print(f"   Dursaa: ...{content[max(0, m2.start()-200):m2.start()]}")

# 4. Yoo scripts wal hin qabanne, sana sirreessi
opens = len(re.findall(r'<script\b[^>]*>', content))
closes = len(re.findall(r'</script>', content))
print(f"\n4. Balance: {opens} opens, {closes} closes, Diff: {opens - closes}")


import os, re

html_path = os.path.expanduser('~/datapulse-web/public/index.html')
app_js_path = os.path.expanduser('~/datapulse-web/public/app.js')

print("=" * 65)
print("🔍 APP.JS DIAGNOSTIC")
print("=" * 65)

# 1. app.js jiraachuu
print(f"\n1. app.js jiraachuu:")
if os.path.exists(app_js_path):
    size = os.path.getsize(app_js_path)
    print(f"   ✅ Jira ({size:,} bytes)")
else:
    print(f"   ❌ HIN JIRU! Combine sun badeera.")
    exit(1)

# 2. app.js keessaa functions
with open(app_js_path, 'r') as f:
    app_js = f.read()

print(f"\n2. app.js keessaa functions:")
for fn in ['function render', 'function vDash', 'function kpis', 'function showLoginFromLanding',
           'function quickDemoLogin', 'function switchAuth', 'function go',
           'var state', 'let state', 'const state', 'window.state',
           'DP.api', 'DP.usage', 'DP.permissions']:
    if fn in app_js:
        print(f"   ✅ {fn}")
    else:
        print(f"   ❌ {fn}")

# 3. index.html keessaa script references
with open(html_path, 'r') as f:
    html = f.read()

print(f"\n3. index.html keessaa script tags:")
for m in re.finditer(r'<script[^>]*>', html):
    line_no = html[:m.start()].count('\n') + 1
    print(f"   Sarara {line_no}: {m.group(0)}")

# 4. app.js load check
if '/app.js' in html or 'app.js' in html:
    print(f"\n4. app.js reference index.html keessatti: ✅ jira")
else:
    print(f"\n4. app.js reference index.html keessatti: ❌ HIN JIRU!")

# 5. app.js syntax check - braces
print(f"\n5. app.js syntax check:")
opens_brace = app_js.count('{')
closes_brace = app_js.count('}')
opens_paren = app_js.count('(')
closes_paren = app_js.count(')')

print(f"   Braces: {{ = {opens_brace}, }} = {closes_brace}, Diff = {opens_brace - closes_brace}")
print(f"   Parens: ( = {opens_paren}, ) = {closes_paren}, Diff = {opens_paren - closes_paren}")

if opens_brace != closes_brace or opens_paren != closes_paren:
    print(f"   ❌ SYNTAX ERROR jira!")
else:
    print(f"   ✅ Balance sirrii dha")

# 6. app.js jalqabaa fi dhumaa
print(f"\n6. app.js jalqabaa (500 chars):")
print(f"   {app_js[:500]}")

print(f"\n7. app.js dhumaa (300 chars):")
print(f"   {app_js[-300:]}")

print("\n" + "=" * 65)

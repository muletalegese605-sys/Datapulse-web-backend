import os, re

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    content = f.read()

print("=" * 60)
print("🔍 RAKKOO DHUGAA - QUICK DEMO LOGIN")
print("=" * 60)

# 1. Button "Quick Demo Login" onclick
print("\n1. Button 'Quick Demo Login' onclick:")
for m in re.finditer(r'<button[^>]*>[\s\S]{0,200}?Quick Demo Login[\s\S]{0,30}?</button>', content):
    line_no = content[:m.start()].count('\n') + 1
    onclick = re.search(r'onclick="([^"]*)"', m.group(0))
    print(f"\n   Sarara {line_no}:")
    print(f"   onclick: {onclick.group(1)[:200] if onclick else '❌ HIN QABU'}")
    break

# 2. quickDemoLogin function keessaa maal akka hojjetu
print("\n2. quickDemoLogin Function keessaa (10 sarara jalqabaa):")
m = re.search(r'function\s+quickDemoLogin\s*\(\s*\)\s*\{', content)
if m:
    start = m.start()
    # Brace count
    depth = 0
    i = m.end() - 1
    end = len(content)
    for j in range(m.end() - 1, len(content)):
        if content[j] == '{': depth += 1
        elif content[j] == '}':
            depth -= 1
            if depth == 0:
                end = j + 1
                break
    fn_body = content[start:end]
    # Sarara jalqabaa 15 agarsiisi
    lines = fn_body.split('\n')[:15]
    for line in lines:
        print(f"   {line[:120]}")

# 3. Element IDs mirkaneessi
print("\n3. Element IDs (function sun itti fayyadama):")
for eid in ['landingPage', 'loginScreen', 'app', 'main', 'loginForm', 'regForm', 'loginEmail', 'loginPass']:
    c = len(re.findall(r'id="' + eid + r'"', content))
    status = '✅' if c > 0 else '❌ HIN JIRU'
    print(f"   #{eid}: {c} {status}")

# 4. state variable ramaduu
print("\n4. state variable ramaduu (assignment):")
state_assigns = re.findall(r'(?:var|let|const|window\.)\s*state\s*=', content)
print(f"   Total: {len(state_assigns)}")
for m in re.finditer(r'(?:var|let|const|window\.)\s*state\s*=', content):
    line_no = content[:m.start()].count('\n') + 1
    print(f"   Sarara {line_no}")

# 5. DP.api jiraachuu
print("\n5. DP.api fi DP.api.loadAll:")
print(f"   DP.api mentions: {content.count('DP.api')}")
print(f"   DP.api.loadAll mentions: {content.count('DP.api.loadAll')}")

# 6. toast function
print("\n6. toast() function:")
print(f"   function toast: {'✅' if 'function toast' in content else '❌'}")

print("\n" + "=" * 60)

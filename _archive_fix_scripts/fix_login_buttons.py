import os, re

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    content = f.read()

# 1. Bakka "Register Org" fi "Quick Demo Login" jiru barbaadi
print("=" * 50)
print("📍 BAKKA BUTTON-WWAN RAKKOO QABAN")
print("=" * 50)

lines = content.split('\n')
for i, line in enumerate(lines, 1):
    if 'Register Org' in line or 'Quick Demo Login' in line:
        print(f"\n📌 Sarara {i}:")
        print(f"   {line.strip()[:200]}")

# 2. Button "Register Org" tiif inline JavaScript (register tab banuuf)
# Bakka: onclick="<function>" jedhu qabate barbaadii, inline JS galchi
content = re.sub(
    r'onclick="[^"]*"[^>]*>(\s*<[^>]*>\s*)*Register Org',
    'onclick="var t=document.getElementById(\'registerTab\');if(t)t.click();if(typeof showRegister===\'function\')showRegister();"',
    content
)

# 3. Button "Quick Demo Login" tiif inline JavaScript (demo login hojjedhu)
# Yeroo tuqtu: login form buusi (fill) gochii, Log In button tuqi
demo_js = (
    "var e=document.getElementById('loginEmail')||document.querySelector('input[type=email]');"
    "var p=document.getElementById('loginPass')||document.querySelector('input[type=password]');"
    "if(e)e.value='demo@datapulse.com';"
    "if(p)p.value='demo1234';"
    "var b=document.getElementById('loginBtn')||document.querySelector('button[onclick*=ogin]');"
    "if(b)b.click();"
    "else if(typeof quickDemoLogin==='function')quickDemoLogin();"
    "else if(typeof demoLogin==='function')demoLogin();"
)
content = re.sub(
    r'onclick="[^"]*"[^>]*>(\s*<[^>]*>\s*)*Quick Demo Login',
    'onclick="' + demo_js + '"',
    content
)

with open(html_path, 'w') as f:
    f.write(content)

print("\n" + "=" * 50)
print("✅ Button-wwan sirreeffamaniiru!")
print("=" * 50)


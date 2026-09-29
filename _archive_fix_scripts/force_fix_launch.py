import os, re

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    content = f.read()

# Inline JavaScript: Landing page dhoksuu, loginScreen banuuf
inline_js = "document.getElementById('landingPage').classList.add('hidden');var ls=document.getElementById('loginScreen');if(ls){ls.classList.remove('hidden');ls.classList.add('flex');}else{var app=document.getElementById('app');if(app)app.classList.remove('hidden');}"

# Button hunda kan onclick="showLoginFromLanding()" qabu, gara inline JavaScript jijjiiri
count = content.count('onclick="showLoginFromLanding()"')
content = content.replace(
    'onclick="showLoginFromLanding()"',
    'onclick="' + inline_js + '"'
)

print(f"✅ Button {count} sirreeffamaniiru!")

# Version counter dabali (cache darbuuf)
if 'window.DP_VERSION' not in content:
    content = content.replace(
        '<script>',
        '<script>\nwindow.DP_VERSION = "' + str(int(os.path.getmtime(html_path))) + '";',
        1
    )
    print("✅ Version counter dabalameera!")

with open(html_path, 'w') as f:
    f.write(content)

print("📍 Amma button tuquun, function call malee, direct DOM manipulation ni hojjeta.")


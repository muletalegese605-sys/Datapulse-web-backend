import os, re

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    content = f.read()

# Bakka 'items = [{id:'SKU-001' ... }];' jiru barbaadii, 'items = [];' taasisuu
pattern = r'items\s*=\s*\[\s*\{\s*id:\s*[\'"]SKU-001[\'"].*?\];'
content_new = re.sub(pattern, 'items = [];', content, flags=re.DOTALL)

if content != content_new:
    with open(html_path, 'w') as f:
        f.write(content_new)
    print("✅ Data sobaa 'items' guutummaatti haqameera!")
else:
    print("⚠️  Data sobaa 'items' hin argamne ykn amma jira.")

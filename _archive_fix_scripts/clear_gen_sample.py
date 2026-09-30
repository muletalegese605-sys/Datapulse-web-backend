import os, re

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    content = f.read()

# Bakka 'function genSample() { return [ ... ]; }' jiru barbaadii, array duwwaa taasisuu
pattern = r'(function genSample\(\)\s*\{\s*return\s*\[).*?(\];)'
content_new = re.sub(pattern, r'\1\2', content, flags=re.DOTALL)

# Yoo state.records = genSample() jiraate, gara state.records = [] jijjiiruu
content_new = content_new.replace('state.records = genSample()', 'state.records = []')

if content != content_new:
    with open(html_path, 'w') as f:
        f.write(content_new)
    print("✅ Data sobaa (Mock) guutummaatti haqameera!")
else:
    print("⚠️  Data sobaa hin argamne ykn amma jira.")

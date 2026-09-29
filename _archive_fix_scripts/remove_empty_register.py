import os

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    lines = f.readlines()

new_lines = []
removed = 0
for line in lines:
    # Yoo sararri 'id="tbRegister"' qabatee, garuu 'Register Org' hin qabaanne, haqi
    if 'id="tbRegister"' in line and 'Register Org' not in line:
        removed += 1
        continue
    new_lines.append(line)

with open(html_path, 'w') as f:
    f.writelines(new_lines)

print(f"✅ Button tbRegister duwwaa {removed} haqameera!")
print(f"📍 Button tbRegister amma {sum(1 for l in new_lines if 'id=\"tbRegister\"' in l)} qofa jira.")

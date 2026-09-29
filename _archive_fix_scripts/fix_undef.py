import os

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    content = f.read()

replacements = {
    '${m.title}': '${m.title || m.name || "Untitled Module"}',
    '${m.category}': '${m.category || "UNCATEGORIZED"}',
    '${m.short}': '${m.short || m.description || "No description"}',
    '${m.description}': '${m.description || m.short || "No description"}',
    '${m.icon}': '${m.icon || "fa-cube"}'
}

count = 0
for old, new in replacements.items():
    if old in content:
        content = content.replace(old, new)
        count += 1

with open(html_path, 'w') as f:
    f.write(content)

print(f"✅ Eegumsi {count} dabalameera. Amma 'UNDEFINED' hin mul'atu.")

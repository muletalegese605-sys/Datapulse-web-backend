import os, re

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    content = f.read()

count = 0

# 1. vCaps() keessatti: advCats filter sirreessi
# Bakka: new Set(ADVANCED_MODULES.map(m => m.category))
# Gara: new Set(ADVANCED_MODULES.filter(m => m && m.category).map(m => m.category))
old_adv = "new Set(ADVANCED_MODULES.map(m => m.category))"
new_adv = "new Set(ADVANCED_MODULES.filter(m => m && m.category).map(m => m.category))"
if old_adv in content:
    content = content.replace(old_adv, new_adv)
    count += 1

# 2. filteredAdv map keessatti: fallback dabaluu
# Bakka: .map(m => { ... ${m.title} ... ${m.category} ... ${m.icon} ... ${m.short} ...
# Gara fallback: ${m.title || 'Untitled'} etc.
replacements = [
    ('${m.title}', '${m.title || m.name || "Untitled Module"}'),
    ('${m.category}', '${m.category || "UNCATEGORIZED"}'),
    ('${m.short}', '${m.short || m.desc || "No description"}'),
    ('${m.icon}', '${m.icon || "fa-cube"}'),
    ('${m.id}', '${m.id || 0}'),
    ('${m.code}', '${m.code || "N/A"}'),
    ('${m.accent}', '${m.accent || "#10b981"}'),
]

for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        count += 1

# 3. vCaps() jalatti: filteredAdv keessaa undefined haquu
old_filter = "const filteredAdv = advModuleFilter === 'All' ? ADVANCED_MODULES : ADVANCED_MODULES.filter(m => m.category === advModuleFilter);"
new_filter = "const filteredAdv = (advModuleFilter === 'All' ? ADVANCED_MODULES : ADVANCED_MODULES.filter(m => m.category === advModuleFilter)).filter(m => m && m.title);"
if old_filter in content:
    content = content.replace(old_filter, new_filter)
    count += 1

# 4. CAPABILITIES map keessatti fallback (yoo jiraate)
cap_replacements = [
    ('${c.title}', '${c.title || c.name || "Untitled"}'),
    ('${c.icon}', '${c.icon || "fa-cube"}'),
    ('${c.desc}', '${c.desc || "No description"}'),
]
for old, new in cap_replacements:
    if old in content and old not in str(replacements):
        content = content.replace(old, new)
        count += 1

with open(html_path, 'w') as f:
    f.write(content)

print(f"✅ Eegumsi {count} dabalameera!")
print("📍 'UNDEFINED' amma hin mul'atu.")

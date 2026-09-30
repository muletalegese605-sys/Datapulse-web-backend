import re
with open('public/index.html', 'r') as f:
    content = f.read()

vars_to_fix = [
    'heights', 'raw', 'rows', 'data', 'insights', 'TABS', 'dock',
    'items', 'stages', 'PLANS', 'labels', 'perms', 'advCats',
    'state.aiChat', 'state.aiFloatingChat'
]

for v in vars_to_fix:
    content = content.replace(f'{v}.map(', f'({v} || []).map(')

content = content.replace('state.notifications.slice(0,20).map(', '(state.notifications || []).slice(0,20).map(')
content = content.replace('this.languages.map(', '(this.languages || []).map(')

with open('public/index.html', 'w') as f:
    f.write(content)
print("Eegumsi hundi dabalameera!")

import os

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    lines = f.readlines()

# Sarara #loginScreen hunda barbaadi
login_lines = [i for i, line in enumerate(lines) if 'id="loginScreen"' in line]
print(f"#loginScreen argameera: {len(login_lines)} sararatti")

if len(login_lines) < 2:
    print("Duplicate hin jiru. Hojii xumurameera.")
    exit()

# Kan lammaffaan jalqabee, sarara </div> column 0 irratti barbaadi
start = login_lines[1]
end = None
for i in range(start + 1, len(lines)):
    stripped = lines[i].rstrip('\n')
    # Yoo sararri ' </div>' jalqabee (column 0), xumura
    if stripped.startswith('</div>') or stripped == '</div>':
        end = i
        break
    # Yoo sararri '<!--' jalqabee (comment), xumura
    if stripped.startswith('<!--') and i > start + 5:
        end = i - 1
        break
    # Yoo sararri element guddaa jalqabee (fkn <section, <footer, </body>)
    if stripped.startswith('<section') or stripped.startswith('<footer') or stripped.startswith('</body>') or stripped.startswith('<script'):
        end = i - 1
        break

if end is None:
    print("Xumura hin argamne - harkaan ilaali")
    print(f"Jalqaba: sarara {start+1}")
    print(f"Koodii jalqabaa: {lines[start].strip()[:150]}")
    print(f"Koodii 5 booda: {lines[start+5].strip()[:150] if start+5 < len(lines) else 'N/A'}")
else:
    print(f"Block: sarara {start+1} hanga {end+1}")
    print(f"Jalqaba: {lines[start].strip()[:100]}")
    print(f"Xumura: {lines[end].strip()[:100]}")
    
    # Haqi
    new_lines = lines[:start] + lines[end+1:]
    
    with open(html_path, 'w') as f:
        f.writelines(new_lines)
    
    print(f"✅ Sarara {end - start + 1} haqameera!")

# Mirkaneessi
with open(html_path, 'r') as f:
    content = f.read()
print(f"\n📍 Amma #loginScreen: {content.count('id=\"loginScreen\"')}")

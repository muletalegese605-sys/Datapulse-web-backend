import os

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    lines = f.readlines()

# Sarara #loginScreen hunda barbaadi
login_lines = []
for i, line in enumerate(lines):
    if 'id="loginScreen"' in line:
        login_lines.append(i)

print(f"=== #loginScreen argameera: {len(login_lines)} sararatti ===")
for i, ln in enumerate(login_lines):
    print(f"   #{i+1}: Sarara {ln+1} (index {ln})")
    print(f"        {lines[ln].strip()[:120]}")

if len(login_lines) > 1:
    # Sarara lammaffaa fi isa booda jiru haqi
    # Start line number (0-indexed)
    second_login_line = login_lines[1]
    
    # Sanarraa jalqabee, 'div' nesting count hojjedhu
    # Opening fi closing divs count
    depth = 0
    started = False
    end_line = None
    
    for i in range(second_login_line, len(lines)):
        line = lines[i]
        # Opening <div
        opens = line.count('<div')
        closes = line.count('</div>')
        
        if not started:
            # Sarara jalqabaa - <div id="loginScreen"
            depth += opens
            started = True
            # Kun yeroo baay'ee <div ...> fi </div> waliin ta'a (single-line)
            if closes > 0:
                depth -= closes
                if depth <= 0:
                    end_line = i
                    break
        else:
            depth += opens
            depth -= closes
            if depth <= 0:
                end_line = i
                break
    
    if end_line:
        print(f"\n📌 Block #loginScreen lammaffaan: Sarara {second_login_line+1} - {end_line+1}")
        print(f"   Jalqabaa: {lines[second_login_line].strip()[:100]}")
        print(f"   Xumura: {lines[end_line].strip()[:100]}")
        
        # Lines haqquuf - line second_login_line irraa hanga end_line
        # Yoo line jalqabaa fi line xumuraa tokko ta'e, tokko qofa haqi
        new_lines = lines[:second_login_line] + lines[end_line+1:]
        
        with open(html_path, 'w') as f:
            f.writelines(new_lines)
        
        removed = end_line - second_login_line + 1
        print(f"\n✅ Sarara {removed} haqameera!")
    else:
        print("\n⚠️  Xumura block hin argamne. Harkaan haquu qabna.")
else:
    print("\n⚠️  Duplicate hin jiru.")

# Mirkaneessi
with open(html_path, 'r') as f:
    new_content = f.read()
final = new_content.count('id="loginScreen"')
print(f"\n📍 Amma #loginScreen: {final}")

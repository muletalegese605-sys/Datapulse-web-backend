import os, re

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    content = f.read()

# Duplicate #loginScreen barbaadii, kan lammaffaa haqi
# Element nesting count fayyadamuun, element guutuu argachuu

def find_all_elements(content, el_id):
    """Element hunda (div/main/section) id waliin barbaadi."""
    results = []
    pattern = re.compile(
        r'<(div|main|section|article|aside|nav)[^>]*id="' + re.escape(el_id) + r'"[^>]*>',
        re.IGNORECASE
    )
    for m in pattern.finditer(content):
        tag_name = m.group(1).lower()
        start = m.start()
        depth = 0
        i = m.end() - 1
        open_pat = '<' + tag_name
        close_pat = '</' + tag_name + '>'
        while i < len(content):
            if content[i:i+len(open_pat)].lower() == open_pat and i+len(open_pat) < len(content) and content[i+len(open_pat)] in ' \t\n>/':
                depth += 1
            elif content[i:i+len(close_pat)].lower() == close_pat:
                if depth == 0:
                    results.append((start, i+len(close_pat), content[start:i+len(close_pat)]))
                    break
                depth -= 1
                i += len(close_pat) - 1
            i += 1
    return results

# #loginScreen hunda barbaadi
logins = find_all_elements(content, 'loginScreen')
print(f"=== #loginScreen argameera: {len(logins)} ===\n")

for i, (start, end, block) in enumerate(logins):
    line_no = content[:start].count('\n') + 1
    print(f"  #{i+1}: Sarara {line_no} ({len(block)} chars)")
    print(f"      {block[:100]}...")

if len(logins) > 1:
    # Kan LAMMAFFAA fi isaan booda jiran haqi, kan JALQABAA dhiisi
    # Reverse order - booda irraa haqi, start position wal hin jijjiiramuuf
    to_remove = sorted(logins[1:], key=lambda x: x[0], reverse=True)
    
    for start, end, block in to_remove:
        content = content[:start] + content[end:]
        print(f"\n🗑️  Sarara {content[:start].count(chr(10))+1} irraa dup haqameera")
    
    print(f"\n✅ #loginScreen {len(to_remove)} haqameera!")
else:
    print("\n⚠️  Duplicate hin jiru.")

with open(html_path, 'w') as f:
    f.write(content)

# Mirkaneessi
final_count = len(re.findall(r'id="loginScreen"', content))
print(f"\n📍 Amma #loginScreen: {final_count}")

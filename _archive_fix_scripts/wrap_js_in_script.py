import os, re

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    content = f.read()

print("=" * 55)
print("🔧 WRAP JS IN SCRIPT TAG")
print("=" * 55)

# 1. Bakka 'function render()' jiru barbaadi
idx_render = content.find('function render(')
if idx_render == -1:
    print("❌ function render() hin argamne!")
    exit(1)

# 2. function render() dura, script tag jiraachuu fi dhabuu mirkaneessi
before = content[:idx_render]
last_open = before.rfind('<script')
last_close = before.rfind('</script>')
in_script = last_open > last_close

print(f"function render() script keessa: {'✅' if in_script else '❌'}")

if not in_script:
    print("\n⚠️  Code sun SCRIPT ALAAAA jira. Wrapping...")
    
    # 3. Bakka JS code sun jalqabu barbaadi
    # Sarara 88 (0-index 87) booda, JS code barbaadi
    # Bifa: '//' comment, 'function', 'const', 'let', 'var', 'window.'
    
    # Last </script> position (char index)
    last_close_pos = before.rfind('</script>') + len('</script>')
    
    # Sana booda, JS code jalqabaa barbaadi
    js_start = last_close_pos
    # Sarara haaraa barbaadi
    while js_start < len(content):
        # Sarara jalqabaa barbaadi
        nl = content.find('\n', js_start)
        if nl == -1:
            break
        line_start = nl + 1
        line_end = content.find('\n', line_start)
        if line_end == -1:
            line_end = len(content)
        line = content[line_start:line_end].strip()
        
        # Yoo sararri JS jalqabaa ta'e (function, const, let, var, //, window, document)
        if re.match(r'^(//|/\*|function\s|const\s|let\s|var\s|window\.|document\.|DP\.|state\s*=|class\s)', line):
            js_start = line_start
            break
        js_start = line_end
    else:
        js_start = last_close_pos
    
    print(f"  JS code jalqabaa: sarara {content[:js_start].count(chr(10)) + 1}")
    
    # 4. JS code xumuraa barbaadi
    # Dhumaa: </body> ykn </html> ykn <script (src waliin) dura
    js_end = content.find('</body>', js_start)
    if js_end == -1:
        js_end = content.find('</html>', js_start)
    if js_end == -1:
        js_end = len(content)
    
    # Yoo sana dura '<script' jiraate (kan biroo), sana dura galchi
    next_script = content.find('<script', js_start)
    if next_script != -1 and next_script < js_end:
        # Yoo script tag kun 'src' hin qaban, dhiisi
        tag_end = content.find('>', next_script)
        tag = content[next_script:tag_end+1]
        if 'src=' not in tag:
            js_end = next_script
    
    print(f"  JS code xumuraa: sarara {content[:js_end].count(chr(10)) + 1}")
    
    # 5. Wrap: <script> ... </script>
    js_block = content[js_start:js_end]
    # Yoo code sun duraan <script> ykn </script> qabaate, sana haqi
    js_block = js_block.strip()
    
    new_content = content[:js_start] + '<script>\n' + js_block + '\n</script>\n' + content[js_end:]
    
    content = new_content
    print(f"  ✅ Code {len(js_block)} chars <script> tag keessatti galmeeffameera")

# 6. Script tags madaallii
opens = len(re.findall(r'<script\b[^>]*>', content))
closes = content.count('</script>')
print(f"\nScript balance: {opens} opens, {closes} closes, Diff = {opens - closes}")

# 7. function render() amma script keessa?
idx_render = content.find('function render(')
if idx_render > 0:
    before = content[:idx_render]
    last_open = before.rfind('<script')
    last_close = before.rfind('</script>')
    in_script = last_open > last_close
    print(f"function render() script keessa: {'✅' if in_script else '❌'}")

with open(html_path, 'w') as f:
    f.write(content)

print("\n" + "=" * 55)
print("📍 MIRKANEESSA")
print("=" * 55)
print(f"<script> tags: {len(re.findall(r'<script\b[^>]*>', content))}")
print(f"</script> tags: {content.count('</script>')}")
print(f"function render() jira: {'✅' if 'function render(' in content else '❌'}")

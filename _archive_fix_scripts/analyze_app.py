import os, re

html_path = os.path.expanduser('~/datapulse-web/public/index.html')
py_path = os.path.expanduser('~/datapulse-backend/main.py')

print("="*50)
print("🚀 DataPulse Codebase Analysis Report")
print("="*50)

if os.path.exists(html_path):
    with open(html_path, 'r') as f: html = f.read()
    print(f"\n📁 FRONTEND: {html_path}")
    
    todos = len(re.findall(r'TODO|FIXME|HACK', html))
    errors = len(re.findall(r'console\.error', html))
    undef = len(re.findall(r'>undefined<|>null<|>NaN<', html))
    mock = len(re.findall(r'mock|dummy|placeholder', html, re.I))
    empty_onclick = len(re.findall(r'onclick=(\"\"|\'\')', html))
    
    print(f"  🔸 TODOs/FIXMEs: {todos}")
    print(f"  🔸 Console Errors: {errors}")
    print(f"  🔸 Undefined/Null UI strings: {undef}")
    print(f"  🔸 Mock/Dummy/Placeholder data: {mock}")
    print(f"  🔸 Empty onclick handlers: {empty_onclick}")

    hardcoded = re.findall(r'>(0|18|40|8) (Total|Used|Runs|Items|Records|Capabilities)<', html, re.I)
    if hardcoded:
        print(f"  ⚠️ Potential hardcoded stats found: {len(hardcoded)}")
        for stat in hardcoded[:5]: print(f"      - Found: '{stat[0]} {stat[1]}'")
else:
    print("\n❌ Frontend index.html not found!")

if os.path.exists(py_path):
    with open(py_path, 'r') as f: py = f.read()
    print(f"\n📁 BACKEND: {py_path}")
    
    py_todos = len(re.findall(r'TODO|FIXME|HACK', py))
    py_pass = len(re.findall(r'def .*:\s*\n\s*pass', py))
    
    # Bakka bu'iinsa: Regex f-string keessaa baafnee variable keessatti galchine
    empty_ret = len(re.findall(r'return\s*\{\}|return\s*\[\]', py))
    try_blocks = len(re.findall(r'try:', py))
    
    print(f"  🔸 TODOs/FIXMEs: {py_todos}")
    print(f"  🔸 Empty routes (pass): {py_pass}")
    print(f"  🔸 Empty returns ({{}} / []): {empty_ret}")
    print(f"  🔸 Try/Except blocks (Error Handling): {try_blocks}")
    
    endpoints = re.findall(r'@app\.(get|post|put|delete)\("([^"]+)"\)', py)
    print(f"\n  📍 Registered Endpoints ({len(endpoints)}):")
    for method, path in endpoints: print(f"      [{method.upper()}] {path}")
else:
    print("\n❌ Backend main.py not found!")

print("\n" + "="*50)
print("✅ Analysis Complete. Check the 🔸 and ⚠️ items.")
print("="*50)

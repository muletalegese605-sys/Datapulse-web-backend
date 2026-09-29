import os, re

py_path = os.path.expanduser('~/datapulse-backend/main.py')

with open(py_path, 'r') as f:
    content = f.read()

# Mirkaneessi: Yoo exception handler jiraate, dhiisi
if 'global_exception_handler' in content:
    print("⚠️  Error handler amma jira. Sirreessuun hin barbaachisu.")
else:
    # 1. Import haaraa dabali (yoo hin jiraanne)
    if 'from fastapi import Request' not in content:
        content = content.replace(
            'from fastapi import FastAPI',
            'from fastapi import FastAPI, Request'
        )
    if 'from fastapi.responses import JSONResponse' not in content:
        content = content.replace(
            'from fastapi.middleware.cors import CORSMiddleware',
            'from fastapi.middleware.cors import CORSMiddleware\nfrom fastapi.responses import JSONResponse'
        )
    
    # 2. Handler koodii qopheessi
    handler_code = '''
# ============ GLOBAL ERROR HANDLER ============
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": str(exc),
            "error_type": type(exc).__name__,
            "path": str(request.url.path)
        }
    )

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"success": False, "error": str(exc), "error_type": "ValueError"}
    )
# ===============================================

'''
    
    # 3. Handler CORS middleware booda galchi
    marker = 'app.add_middleware(\n    CORSMiddleware,'
    if marker in content:
        # CORS block xumura isaa barbaadi
        idx = content.find(marker)
        # Bracket dhiphinaa lammaffaa barbaadi
        end_marker = content.find(')\n', idx)
        # Bracket lammaffaa barbaaduu
        count = 0
        i = idx
        while i < len(content):
            if content[i] == '(':
                count += 1
            elif content[i] == ')':
                count -= 1
                if count == 0:
                    end_marker = i + 1
                    break
            i += 1
        
        content = content[:end_marker] + '\n' + handler_code + content[end_marker:]
    else:
        # Yoo marker hin argamne, root endpoint dura galchi
        content = content.replace(
            '@app.get("/")',
            handler_code + '@app.get("/")'
        )
    
    with open(py_path, 'w') as f:
        f.write(content)
    
    print("✅ Error handler sirriitti dabalameera!")
    print("📍 Endpoint hundaaf of eeggannoo ni kenna.")


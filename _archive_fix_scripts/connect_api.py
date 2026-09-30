import os

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    content = f.read()

if 'DP.api' in content:
    print("⚠️  DP.api module amma jira. Sirreessuun hin barbaachisu.")
else:
    api_module = '''
// ========== BACKEND API INTEGRATION ==========
DP.api = {
    base: 'https://datapulse-web-backend.onrender.com',
    _cache: { records: [], usage: { used: 0, runs: 0 } },
    
    fetchRecords: async function() {
        try {
            const res = await fetch(this.base + '/api/records?t=' + Date.now());
            const data = await res.json();
            if (data.success) {
                this._cache.records = data.records || [];
                state.records = this._cache.records;
                return this._cache.records;
            }
        } catch(e) { console.warn('API records fetch failed:', e.message); }
        return this._cache.records;
    },
    
    fetchUsage: async function() {
        try {
            const res = await fetch(this.base + '/api/usage?t=' + Date.now());
            const data = await res.json();
            if (data.success) {
                this._cache.usage = { used: data.used || 0, runs: data.runs || 0 };
                return this._cache.usage;
            }
        } catch(e) { console.warn('API usage fetch failed:', e.message); }
        return this._cache.usage;
    },
    
    postUsage: async function() {
        try {
            const res = await fetch(this.base + '/api/usage/increment', { method: 'POST' });
            const data = await res.json();
            if (data.success) {
                this._cache.usage = { used: data.used, runs: data.runs };
            }
        } catch(e) { console.warn('API usage post failed:', e.message); }
    },
    
    addRecord: async function(rec) {
        try {
            const res = await fetch(this.base + '/api/records', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(rec)
            });
            const data = await res.json();
            if (data.success) {
                await this.fetchRecords();
                return data.record;
            }
        } catch(e) { console.warn('API add record failed:', e.message); }
        return null;
    },
    
    loadAll: async function() {
        if (typeof toast === 'function') toast('Loading data from server...', 'info');
        await Promise.all([ this.fetchRecords(), this.fetchUsage() ]);
        if (typeof render === 'function') render();
        if (typeof toast === 'function') toast('Data loaded ✓', 'success');
    }
};
// ============================================
'''

    # 1. Galchi DP.api module
    if '// ========== PERMISSIONS MODULE ==========' in content:
        content = content.replace('// ========== PERMISSIONS MODULE ==========', api_module + '\n// ========== PERMISSIONS MODULE ==========', 1)
    elif '// ========== USAGE TRACKING ==========' in content:
        content = content.replace('// ========== USAGE TRACKING ==========', api_module + '\n// ========== USAGE TRACKING ==========', 1)
    else:
        content = content.replace('DP.theme', api_module + '\nDP.theme', 1)

    # 2. DP.usage.getStats — backend cache fayyadami
    old_gs = "getStats: function() {\n        try { return JSON.parse(localStorage.getItem('dp_usage')) || {used:0, runs:0}; }\n        catch(e) { return {used:0, runs:0}; }\n    },"
    new_gs = "getStats: function() {\n        if (window.DP && DP.api && DP.api._cache && DP.api._cache.usage) return DP.api._cache.usage;\n        try { return JSON.parse(localStorage.getItem('dp_usage')) || {used:0, runs:0}; }\n        catch(e) { return {used:0, runs:0}; }\n    },"
    if old_gs in content:
        content = content.replace(old_gs, new_gs, 1)
    else:
        # fallback: regex
        content = content.replace("getStats: function() {", "getStats: function() {\n        if (window.DP && DP.api && DP.api._cache && DP.api._cache.usage) return DP.api._cache.usage;", 1)

    # 3. DP.usage.increment — backend irrattis galmeessi
    old_inc = "increment: function() {\n        const s = this.getStats();\n        s.used += 1;\n        s.runs += 1;\n        localStorage.setItem('dp_usage', JSON.stringify(s));\n        return s;\n    },"
    new_inc = "increment: function() {\n        const s = this.getStats();\n        s.used += 1;\n        s.runs += 1;\n        localStorage.setItem('dp_usage', JSON.stringify(s));\n        if (window.DP && DP.api && DP.api.postUsage) DP.api.postUsage();\n        return s;\n    },"
    if old_inc in content:
        content = content.replace(old_inc, new_inc, 1)
    else:
        content = content.replace("increment: function() {", "increment: function() {\n        if (window.DP && DP.api && DP.api.postUsage) DP.api.postUsage();", 1)

    # 4. INIT keessatti DP.api.loadAll() dabalii
    if 'DP.api.loadAll()' not in content:
        old_init = "DP.i18n.apply();"
        new_init = "DP.i18n.apply();\n        if (window.DP && DP.api) DP.api.loadAll();"
        if old_init in content:
            content = content.replace(old_init, new_init, 1)

    with open(html_path, 'w') as f:
        f.write(content)
    
    print("✅ Frontend-Backend integration dabalameera!")
    print("📍 state.records, DP.usage amma backend irraa dhufu.")


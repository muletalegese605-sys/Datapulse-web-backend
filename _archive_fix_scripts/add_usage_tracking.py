import os, re

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    content = f.read()

if 'dp_usage' in content:
    print("⚠️  Usage tracking amma jira. Sirreessuun hin barbaachisu.")
else:
    # 1. DP.usage module uumii (DP object jalatti)
    usage_module = """
// ========== USAGE TRACKING ==========
DP.usage = {
    getStats: function() {
        try { return JSON.parse(localStorage.getItem('dp_usage')) || {used:0, runs:0}; }
        catch(e) { return {used:0, runs:0}; }
    },
    increment: function() {
        const s = this.getStats();
        s.used += 1;
        s.runs += 1;
        localStorage.setItem('dp_usage', JSON.stringify(s));
        return s;
    },
    reset: function() {
        localStorage.setItem('dp_usage', JSON.stringify({used:0, runs:0}));
    }
};
// ======================================
"""
    
    # Bakka 'DP.theme' jiru barbaadii, dura isaa galchi
    if 'DP.theme' in content:
        content = content.replace('DP.theme', usage_module + 'DP.theme', 1)
    else:
        # Yoo DP.theme hin argamne, INIT dura galchi
        content = content.replace(
            'window.addEventListener(\'DOMContentLoaded\'',
            usage_module + 'window.addEventListener(\'DOMContentLoaded\'',
            1
        )
    
    # 2. Stats lakkoofsa 'USED' fi 'RUNS' localStorage irraa akka dubbisu
    # Suuraa duraa irratti: "0 USED" fi "0 RUNS" hardcoded ture. Amma dynamic taasisuu
    content = content.replace(
        '<div class="text-base font-bold text-sky-400 mono">${usedModules}</div>',
        '<div class="text-base font-bold text-sky-400 mono">${DP.usage.getStats().used}</div>'
    )
    content = content.replace(
        '<div class="text-base font-bold text-amber-400 mono">${totalRuns}</div>',
        '<div class="text-base font-bold text-amber-400 mono">${DP.usage.getStats().runs}</div>'
    )
    
    # 3. 'runAdvancedModule' function keessatti usage increment dabaluu
    if 'function runAdvancedModule' in content:
        content = content.replace(
            'function runAdvancedModule(id){',
            'function runAdvancedModule(id){ DP.usage.increment();'
        )
    
    # 4. 'runCap' function keessatti usage increment dabaluu
    if 'function runCap' in content:
        content = content.replace(
            'function runCap(fn){',
            'function runCap(fn){ DP.usage.increment();'
        )
    
    with open(html_path, 'w') as f:
        f.write(content)
    
    print("✅ Usage tracking (dp_usage) sirriitti dabalameera!")
    print("📍 Yeroo module hojjettu, USED fi RUNS ni jijjiiramu.")


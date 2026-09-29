import os, re

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    content = f.read()

print("=" * 65)
print("🔧 DP.USAGE MODULE DABALUU")
print("=" * 65)

# ============================================================
# 1. DP.usage module uumii
# ============================================================
if 'DP.usage' not in content or 'getStats: function' not in content:
    usage_module = '''
// ========== USAGE TRACKING MODULE ==========
if (typeof DP === 'undefined') window.DP = {};

DP.usage = {
  _cache: {used: 0, runs: 0},
  
  getStats: function() {
    // Backend cache irraa dubbisi
    if (this._cache && (this._cache.used > 0 || this._cache.runs > 0)) {
      return {used: this._cache.used, runs: this._cache.runs};
    }
    // localStorage irraa dubbisi
    try {
      var s = JSON.parse(localStorage.getItem('dp_usage'));
      if (s && typeof s.used === 'number') return s;
    } catch(e) {}
    return {used: 0, runs: 0};
  },
  
  increment: function() {
    try {
      var s = this.getStats();
      s.used = (s.used || 0) + 1;
      s.runs = (s.runs || 0) + 1;
      this._cache = s;
      localStorage.setItem('dp_usage', JSON.stringify(s));
      
      // Backend irrattis galmeessi (yoo jiraate)
      this.syncToBackend();
      
      // UI refresh
      if (typeof render === 'function') {
        try { render(); } catch(e) {}
      }
      return s;
    } catch(e) {
      console.warn('DP.usage.increment error:', e.message);
      return {used: 0, runs: 0};
    }
  },
  
  syncToBackend: function() {
    try {
      var base = (typeof DP.api !== 'undefined' && DP.api.base) ? DP.api.base : 'https://datapulse-web-backend.onrender.com';
      fetch(base + '/api/usage/increment', {method: 'POST'}).catch(function(){});
    } catch(e) {}
  },
  
  fetchFromBackend: function() {
    var self = this;
    try {
      var base = (typeof DP.api !== 'undefined' && DP.api.base) ? DP.api.base : 'https://datapulse-web-backend.onrender.com';
      return fetch(base + '/api/usage?t=' + Date.now())
        .then(function(r){ return r.json(); })
        .then(function(data){
          if (data && data.success) {
            self._cache = {used: data.used || 0, runs: data.runs || 0};
            localStorage.setItem('dp_usage', JSON.stringify(self._cache));
          }
          return self._cache;
        })
        .catch(function(){ return self._cache; });
    } catch(e) {
      return Promise.resolve(self._cache);
    }
  },
  
  reset: function() {
    this._cache = {used: 0, runs: 0};
    localStorage.setItem('dp_usage', JSON.stringify(this._cache));
    if (typeof render === 'function') { try { render(); } catch(e) {} }
  }
};

// Yeroo app banamu, backend irraa usage fidu
window.addEventListener('load', function() {
  setTimeout(function() {
    if (DP && DP.usage && DP.usage.fetchFromBackend) DP.usage.fetchFromBackend();
  }, 2000);
});
// =============================================
'''

    # Bakka '</script>' isa jalqabaa (kan script guddaa) dura galchi
    # Mala gaarii: 'window.addEventListener(\'DOMContentLoaded\'' dura galchi
    if "window.addEventListener('DOMContentLoaded'" in content:
        content = content.replace(
            "window.addEventListener('DOMContentLoaded'",
            usage_module + "\nwindow.addEventListener('DOMContentLoaded'",
            1
        )
        print("✅ DP.usage module dabalameera (DOMContentLoaded dura)")
    else:
        # Fallback: </script> isa dhumaa dura
        last_close = content.rfind('</script>')
        if last_close > 0:
            content = content[:last_close] + usage_module + '\n' + content[last_close:]
            print("✅ DP.usage module dabalameera (</script> dura)")
else:
    print("⚠️  DP.usage module amma jira.")

# ============================================================
# 2. runAdvancedModule fi runCap functions waliin walqabsiisi
# ============================================================
# runAdvancedModule function - usage increment dabaluu
if 'function runAdvancedModule' in content:
    # Yoo 'DP.usage.increment' hin jiraanne
    m = re.search(r'function\s+runAdvancedModule\s*\([^)]*\)\s*\{', content)
    if m:
        # Bracket balance - function xumura barbaadi
        start = m.start()
        depth = 0
        end = start
        for i in range(m.end() - 1, len(content)):
            if content[i] == '{': depth += 1
            elif content[i] == '}':
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
        fn_body = content[start:end]
        if 'DP.usage.increment' not in fn_body:
            # Function jalqabaa booda DP.usage.increment() dabaluu
            new_fn = fn_body.replace(
                m.group(0),
                m.group(0) + '\n  try { if (typeof DP !== "undefined" && DP.usage) DP.usage.increment(); } catch(e) {}',
                1
            )
            content = content.replace(fn_body, new_fn, 1)
            print("✅ runAdvancedModule: DP.usage.increment() dabalameera")

# runCap function - usage increment dabaluu
if 'function runCap' in content:
    m = re.search(r'function\s+runCap\s*\([^)]*\)\s*\{', content)
    if m:
        start = m.start()
        depth = 0
        end = start
        for i in range(m.end() - 1, len(content)):
            if content[i] == '{': depth += 1
            elif content[i] == '}':
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
        fn_body = content[start:end]
        if 'DP.usage.increment' not in fn_body:
            new_fn = fn_body.replace(
                m.group(0),
                m.group(0) + '\n  try { if (typeof DP !== "undefined" && DP.usage) DP.usage.increment(); } catch(e) {}',
                1
            )
            content = content.replace(fn_body, new_fn, 1)
            print("✅ runCap: DP.usage.increment() dabalameera")

# ============================================================
# 3. Stats display - 'USED' fi 'RUNS' DP.usage irraa dubbisi
# ============================================================
# Bakka '0 USED' ykn '${usedModules}' fi '${totalRuns}' jiru barbaadi
# Suuraa duraa irratti: '${usedModules}' fi '${totalRuns}' turan

# usedModules variable
if '${usedModules}' in content:
    content = content.replace('${usedModules}', '${(DP.usage.getStats().used || 0)}')
    print("✅ ${usedModules} → DP.usage.getStats().used")

# totalRuns variable
if '${totalRuns}' in content:
    content = content.replace('${totalRuns}', '${(DP.usage.getStats().runs || 0)}')
    print("✅ ${totalRuns} → DP.usage.getStats().runs")

# 'const usedModules = ...' barbaadii, DP.usage waliin bakka buusi
content = re.sub(
    r'const\s+usedModules\s*=\s*Object\.keys\(advModuleRuns\)\.length;',
    'const usedModules = (typeof DP !== "undefined" && DP.usage) ? DP.usage.getStats().used : Object.keys(advModuleRuns).length;',
    content
)

content = re.sub(
    r'const\s+totalRuns\s*=\s*Object\.values\(advModuleRuns\)\.reduce\(\(a,b\)=>a\+b,0\);',
    'const totalRuns = (typeof DP !== "undefined" && DP.usage) ? DP.usage.getStats().runs : Object.values(advModuleRuns).reduce((a,b)=>a+b,0);',
    content
)

print("✅ Stats display DP.usage waliin bakka bu'ameera")

# ============================================================
# 4. Mirkaneessi
# ============================================================
with open(html_path, 'w') as f:
    f.write(content)

with open(html_path, 'r') as f:
    new_content = f.read()

print("\n" + "=" * 65)
print("📍 MIRKANEESSA")
print("=" * 65)

print(f"   DP.usage mentions: {new_content.count('DP.usage')}")
print(f"   DP.usage.increment: {new_content.count('DP.usage.increment')}")
print(f"   DP.usage.getStats: {new_content.count('DP.usage.getStats')}")
print(f"   DP.usage.fetchFromBackend: {new_content.count('DP.usage.fetchFromBackend')}")

# Script balance
opens = len(re.findall(r'<script\b[^>]*>', new_content))
closes = new_content.count('</script>')
print(f"\n   Script balance: {opens} / {closes}, Diff: {opens - closes}")

# functions check
for fn in ['DP.usage.getStats', 'DP.usage.increment', 'DP.usage.fetchFromBackend']:
    if fn in new_content:
        print(f"   ✅ {fn}")

print("\n" + "=" * 65)
print("✅ XUMURAMEERA!")
print("=" * 65)

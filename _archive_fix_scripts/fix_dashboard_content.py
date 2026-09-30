import os, re

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    content = f.read()

print("=" * 65)
print("🔧 DASHBOARD CONTENT GUUTUU")
print("=" * 65)

# ============================================================
# 1. DP.api module - backend irraa data fidu (yoo hin jiraanne)
# ============================================================
if 'DP.api' not in content or 'fetchRecords' not in content:
    api_module = '''
// ========== BACKEND API INTEGRATION ==========
if (typeof DP === 'undefined') window.DP = {};

DP.api = {
  base: 'https://datapulse-web-backend.onrender.com',
  _cache: { records: [], usage: {used:0, runs:0}, loaded: false },
  
  fetchRecords: function() {
    var self = this;
    try {
      return fetch(this.base + '/api/records?t=' + Date.now())
        .then(function(r){ return r.json(); })
        .then(function(data){
          if (data && data.success && Array.isArray(data.records)) {
            self._cache.records = data.records;
            if (typeof state !== 'undefined') {
              state.records = data.records;
            }
            self._cache.loaded = true;
            return data.records;
          }
          return self._cache.records;
        })
        .catch(function(e){ console.warn('fetchRecords err:', e.message); return self._cache.records; });
    } catch(e) { return Promise.resolve(self._cache.records); }
  },
  
  fetchUsage: function() {
    var self = this;
    try {
      return fetch(this.base + '/api/usage?t=' + Date.now())
        .then(function(r){ return r.json(); })
        .then(function(data){
          if (data && data.success) {
            self._cache.usage = {used: data.used || 0, runs: data.runs || 0};
            if (typeof DP.usage !== 'undefined') {
              DP.usage._cache = self._cache.usage;
            }
          }
          return self._cache.usage;
        })
        .catch(function(){ return self._cache.usage; });
    } catch(e) { return Promise.resolve(self._cache.usage); }
  },
  
  addRecord: function(rec) {
    var self = this;
    try {
      return fetch(this.base + '/api/records', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(rec)
      })
      .then(function(r){ return r.json(); })
      .then(function(data){
        if (data && data.success) {
          self._cache.records.push(data.record);
          if (typeof state !== 'undefined') state.records = self._cache.records;
          return data.record;
        }
        return null;
      })
      .catch(function(){ return null; });
    } catch(e) { return Promise.resolve(null); }
  },
  
  loadAll: function() {
    var self = this;
    return Promise.all([this.fetchRecords(), this.fetchUsage()])
      .then(function() {
        // Render deebi'ee hojjedhu
        if (typeof render === 'function') {
          try { render(); } catch(e) { console.warn('render after load err:', e.message); }
        }
        return self._cache;
      })
      .catch(function(e) { console.warn('loadAll err:', e.message); });
  }
};

// Yeroo app banamu, data fidu
window.addEventListener('load', function() {
  setTimeout(function() {
    if (DP && DP.api && DP.api.loadAll) {
      DP.api.loadAll().then(function() {
        console.log('✅ Backend data loaded');
      });
    }
  }, 1500);
});

// Yeroo login/demo tuqtu, ammas data fidu
document.addEventListener('click', function(ev) {
  var t = ev.target.closest('button');
  if (!t) return;
  var txt = (t.textContent || '').trim().toLowerCase();
  if (txt.indexOf('quick demo login') !== -1 || txt === 'log in') {
    setTimeout(function() {
      if (DP && DP.api && DP.api.loadAll) DP.api.loadAll();
    }, 1200);
  }
}, true);
// =============================================
'''
    # Bakka 'DOMContentLoaded' dura galchi
    if "window.addEventListener('DOMContentLoaded'" in content:
        content = content.replace(
            "window.addEventListener('DOMContentLoaded'",
            api_module + "\nwindow.addEventListener('DOMContentLoaded'",
            1
        )
        print("✅ DP.api module dabalameera")
    else:
        last_close = content.rfind('</script>')
        if last_close > 0:
            content = content[:last_close] + api_module + '\n' + content[last_close:]
            print("✅ DP.api module dabalameera (</script> dura)")

# ============================================================
# 2. render() function - data hin qabu ta'e fallback kenna
# ============================================================
# render() keessatti, yoo state.records duwwaa ta'e, data fiduu
render_m = re.search(r'function\s+render\s*\(\s*\)\s*\{', content)
if render_m:
    start = render_m.start()
    depth = 0
    end = start
    for i in range(render_m.end() - 1, len(content)):
        if content[i] == '{': depth += 1
        elif content[i] == '}':
            depth -= 1
            if depth == 0:
                end = i + 1
                break
    render_fn = content[start:end]
    
    if 'DP.api.loadAll' not in render_fn and 'DP.api.fetchRecords' not in render_fn:
        # Function dhuma booda, data fetch dabaluu
        new_render = render_fn.replace(
            'if (window.DP && DP.api && DP.api.loadAll && !window._dpLoading) { window._dpLoading = true; DP.api.loadAll().finally(function(){ window._dpLoading = false; }); }',
            'if (window.DP && DP.api && DP.api.loadAll && !window._dpLoading) { window._dpLoading = true; DP.api.loadAll().finally(function(){ window._dpLoading = false; }); } else if (window.DP && DP.api && DP.api.fetchRecords && !window._dpLoading) { window._dpLoading = true; DP.api.fetchRecords().then(function() { window._dpLoading = false; if (typeof render === "function") render(); }); }'
        )
        if new_render != render_fn:
            content = content.replace(render_fn, new_render, 1)
            print("✅ render(): data fetch fallback dabalameera")
        else:
            # Yoo sana hin argamne, function jalqabaa booda dabaluu
            new_render = render_fn.replace(
                render_m.group(0),
                render_m.group(0) + '\n  setTimeout(function(){ if (window.DP && DP.api && DP.api.fetchRecords && !window._dpLoading) { window._dpLoading = true; DP.api.fetchRecords().then(function(){ window._dpLoading = false; if (typeof render === "function" && !window._rendering) { window._rendering = true; render(); window._rendering = false; } }); } }, 500);',
                1
            )
            content = content.replace(render_fn, new_render, 1)
            print("✅ render(): data fetch fallback dabalameera (jalqabaa booda)")

# ============================================================
# 3. vDash() keessatti - data duwwaa ta'e fallback content
# ============================================================
vDash_m = re.search(r'function\s+vDash\s*\([^)]*\)\s*\{', content)
if vDash_m:
    start = vDash_m.start()
    depth = 0
    end = start
    for i in range(vDash_m.end() - 1, len(content)):
        if content[i] == '{': depth += 1
        elif content[i] == '}':
            depth -= 1
            if depth == 0:
                end = i + 1
                break
    vdash_fn = content[start:end]
    
    # Yoo vDash keessaa state.records.length === 0 fallback hin qabu
    if 'state.records.length === 0' not in vdash_fn and 'records.length' not in vdash_fn:
        # Function jalqabaa booda, records check dabaluu
        new_vdash = vdash_fn.replace(
            vDash_m.group(0),
            vDash_m.group(0) + '''
  // Yoo records duwwaa ta'e, fallback dashboard agarsiisi
  try {
    if (typeof state === "undefined" || !state.records || state.records.length === 0) {
      var noDataHtml = '<div class="p-4 space-y-4">' +
        '<div class="bg-emerald-500/10 border border-emerald-500/30 rounded-2xl p-4">' +
        '<div class="flex items-center gap-2 mb-3">' +
        '<i class="fa-solid fa-database text-emerald-400 text-xl"></i>' +
        '<div><h3 class="text-base font-bold text-white">No data yet</h3>' +
        '<p class="text-[11px] text-slate-400">Upload a CSV or connect a data source to see insights</p></div>' +
        '</div>' +
        '<button type="button" onclick="go(\\'sources\\')" class="w-full py-2 bg-emerald-500 text-slate-950 rounded-xl font-bold text-xs">' +
        '<i class="fa-solid fa-plus mr-1"></i>Add Data Source' +
        '</button>' +
        '</div>' +
        '<div class="grid grid-cols-2 gap-3">' +
        '<div class="bg-slate-900/70 border border-slate-800 rounded-2xl p-4">' +
        '<p class="text-[10px] text-slate-400 uppercase mb-1">Total Records</p>' +
        '<p class="text-2xl font-bold text-emerald-400 mono">0</p></div>' +
        '<div class="bg-slate-900/70 border border-slate-800 rounded-2xl p-4">' +
        '<p class="text-[10px] text-slate-400 uppercase mb-1">Gross Sales</p>' +
        '<p class="text-2xl font-bold text-sky-400 mono">ETB 0</p></div>' +
        '<div class="bg-slate-900/70 border border-slate-800 rounded-2xl p-4">' +
        '<p class="text-[10px] text-slate-400 uppercase mb-1">Margin</p>' +
        '<p class="text-2xl font-bold text-amber-400 mono">0%</p></div>' +
        '<div class="bg-slate-900/70 border border-slate-800 rounded-2xl p-4">' +
        '<p class="text-[10px] text-slate-400 uppercase mb-1">Low Stock</p>' +
        '<p class="text-2xl font-bold text-rose-400 mono">0</p></div>' +
        '</div>' +
        '<div class="bg-slate-900/70 border border-slate-800 rounded-2xl p-4">' +
        '<p class="text-[10px] text-slate-400 uppercase mb-2">Available Capabilities</p>' +
        '<div class="grid grid-cols-4 gap-2 text-center">' +
        '<div><i class="fa-solid fa-file-csv text-emerald-400"></i><p class="text-[9px] text-slate-400 mt-1">CSV/Excel</p></div>' +
        '<div><i class="fa-solid fa-link text-sky-400"></i><p class="text-[9px] text-slate-400 mt-1">Link/URL</p></div>' +
        '<div><i class="fa-solid fa-plug text-purple-400"></i><p class="text-[9px] text-slate-400 mt-1">REST API</p></div>' +
        '<div><i class="fa-solid fa-microchip text-amber-400"></i><p class="text-[9px] text-slate-400 mt-1">IoT</p></div>' +
        '</div></div></div>';
      return noDataHtml;
    }
  } catch(e) { console.warn('vDash fallback err:', e.message); }
''',
            1
        )
        if new_vdash != vdash_fn:
            content = content.replace(vdash_fn, new_vdash, 1)
            print("✅ vDash(): no-data fallback dabalameera")

# ============================================================
# 4. Backup: Yeroo app banamu data fidi (yoo hin fidne)
# ============================================================
backup_fetch = '''
// ========== DATA FETCH BACKUP ==========
(function() {
  var attempts = 0;
  var timer = setInterval(function() {
    attempts++;
    if (attempts > 20) { clearInterval(timer); return; }
    try {
      if (window.DP && DP.api && DP.api.fetchRecords) {
        var main = document.getElementById('main');
        var app = document.getElementById('app');
        if (main && app && !app.classList.contains('hidden')) {
          // Yoo dashboard visible ta'e, data fidu
          if (main.innerHTML.length < 500) {
            DP.api.fetchRecords().then(function() {
              if (typeof render === 'function') {
                try { render(); } catch(e) {}
              }
            });
          }
        }
      }
    } catch(e) {}
  }, 3000);
})();
// ======================================
'''

if 'DATA FETCH BACKUP' not in content:
    last_close = content.rfind('</script>')
    if last_close > 0:
        content = content[:last_close] + backup_fetch + '\n' + content[last_close:]
        print("✅ Data fetch backup dabalameera")

# ============================================================
# Save
# ============================================================
with open(html_path, 'w') as f:
    f.write(content)

# ============================================================
# MIRKANEESSA
# ============================================================
with open(html_path, 'r') as f:
    new_content = f.read()

print("\n" + "=" * 65)
print("📍 MIRKANEESSA")
print("=" * 65)

print(f"   DP.api mentions: {new_content.count('DP.api')}")
print(f"   DP.api.fetchRecords: {new_content.count('DP.api.fetchRecords')}")
print(f"   DP.api.loadAll: {new_content.count('DP.api.loadAll')}")
print(f"   No-data fallback: {'✅' if 'No data yet' in new_content else '❌'}")
print(f"   Data fetch backup: {'✅' if 'DATA FETCH BACKUP' in new_content else '❌'}")

opens = len(re.findall(r'<script\b[^>]*>', new_content))
closes = new_content.count('</script>')
print(f"\n   Script balance: {opens} / {closes}, Diff: {opens - closes}")

print("\n" + "=" * 65)
print("✅ XUMURAMEERA!")
print("=" * 65)

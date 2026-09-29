import os, re

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    content = f.read()

print("=" * 65)
print("🔧 MODULES HAARAA DABALUU")
print("=" * 65)

modules_script = '''
// ============================================================
// ========== DATAPULSE MODULES (RESTORED) ===================
// ============================================================

// ========== DP.api MODULE ==========
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
            if (typeof state !== 'undefined') state.records = data.records;
            return data.records;
          }
          return self._cache.records;
        })
        .catch(function(){ return self._cache.records; });
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
            if (typeof DP.usage !== 'undefined') DP.usage._cache = self._cache.usage;
          }
          return self._cache.usage;
        })
        .catch(function(){ return self._cache.usage; });
    } catch(e) { return Promise.resolve(self._cache.usage); }
  },
  
  loadAll: function() {
    var self = this;
    return Promise.all([this.fetchRecords(), this.fetchUsage()])
      .then(function() {
        if (typeof render === 'function') { try { render(); } catch(e) {} }
        return self._cache;
      })
      .catch(function(e) { console.warn('loadAll err:', e.message); });
  }
};

// Yeroo app banamu data fidu
window.addEventListener('load', function() {
  setTimeout(function() { if (DP && DP.api && DP.api.loadAll) DP.api.loadAll(); }, 1500);
});

// ========== DP.usage MODULE ==========
DP.usage = {
  _cache: {used: 0, runs: 0},
  getStats: function() {
    if (this._cache && (this._cache.used > 0 || this._cache.runs > 0)) return this._cache;
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
      try {
        var base = (DP.api && DP.api.base) ? DP.api.base : 'https://datapulse-web-backend.onrender.com';
        fetch(base + '/api/usage/increment', {method: 'POST'}).catch(function(){});
      } catch(e) {}
      if (typeof render === 'function') { try { render(); } catch(e) {} }
      return s;
    } catch(e) { return {used: 0, runs: 0}; }
  }
};

// ========== DP.permissions MODULE ==========
DP.permissions = {
  _cache: {},
  map: {
    'Internet': 'internet', 'Camera': 'camera', 'Microphone': 'microphone',
    'Location': 'location', 'Notifications': 'notifications', 'Storage': 'storage'
  },
  getState: function(key) {
    try {
      if (key === 'internet') return navigator.onLine ? 'ON' : 'OFF';
      if (key === 'notifications') {
        return ('Notification' in window && Notification.permission === 'granted') ? 'ON' : 'OFF';
      }
      var stored = localStorage.getItem('dp_perm_' + key);
      return (stored === 'granted') ? 'ON' : 'OFF';
    } catch(e) { return 'OFF'; }
  },
  request: function(key) {
    var self = this;
    return new Promise(function(resolve) {
      try {
        if (key === 'internet') { resolve(navigator.onLine); return; }
        if (key === 'camera') {
          if (!navigator.mediaDevices) { resolve(false); return; }
          navigator.mediaDevices.getUserMedia({video: true})
            .then(function(s){ s.getTracks().forEach(function(t){t.stop();}); localStorage.setItem('dp_perm_camera','granted'); resolve(true); })
            .catch(function(){ localStorage.setItem('dp_perm_camera','denied'); resolve(false); });
          return;
        }
        if (key === 'microphone') {
          if (!navigator.mediaDevices) { resolve(false); return; }
          navigator.mediaDevices.getUserMedia({audio: true})
            .then(function(s){ s.getTracks().forEach(function(t){t.stop();}); localStorage.setItem('dp_perm_microphone','granted'); resolve(true); })
            .catch(function(){ localStorage.setItem('dp_perm_microphone','denied'); resolve(false); });
          return;
        }
        if (key === 'location') {
          if (!navigator.geolocation) { resolve(false); return; }
          navigator.geolocation.getCurrentPosition(
            function(){ localStorage.setItem('dp_perm_location','granted'); resolve(true); },
            function(){ localStorage.setItem('dp_perm_location','denied'); resolve(false); },
            {timeout: 10000}
          );
          return;
        }
        if (key === 'notifications') {
          if (!('Notification' in window)) { resolve(false); return; }
          Notification.requestPermission().then(function(p){
            if (p === 'granted') { localStorage.setItem('dp_perm_notifications','granted'); resolve(true); }
            else { localStorage.setItem('dp_perm_notifications','denied'); resolve(false); }
          });
          return;
        }
        if (key === 'storage') {
          if (navigator.storage && navigator.storage.persist) {
            navigator.storage.persist().then(function(ok){
              if (ok) { localStorage.setItem('dp_perm_storage','granted'); resolve(true); }
              else { localStorage.setItem('dp_perm_storage','denied'); resolve(false); }
            });
          } else { resolve(false); }
          return;
        }
        resolve(false);
      } catch(e) { resolve(false); }
    });
  }
};

// ========== quickDemoLogin FUNCTION ==========
function quickDemoLogin(){
  try {
    localStorage.setItem('dp_demo_user', JSON.stringify({name:'Demo Admin',email:'demo@datapulse.com',role:'admin'}));
    var lp = document.getElementById('landingPage'); if (lp) lp.classList.add('hidden');
    var ls = document.getElementById('loginScreen'); if (ls) ls.classList.add('hidden');
    var app = document.getElementById('app'); if (app) { app.classList.remove('hidden'); app.style.display=''; }
    var main = document.getElementById('main'); if (main) { main.classList.remove('hidden'); main.style.display=''; }
    if (typeof state !== 'undefined') {
      state.user = {name:'Demo Admin',email:'demo@datapulse.com',role:'admin'};
      state.org = {id:'ORG-DEMO',name:'Demo Enterprise'};
      if (!state.tab) state.tab = 'dashboard';
      if (!Array.isArray(state.records)) state.records = [];
    }
    if (typeof render === 'function') { try { render(); } catch(e) { console.warn('render err:', e.message); } }
    try { if (DP && DP.api && DP.api.loadAll) DP.api.loadAll(); } catch(e) {}
    if (typeof toast === 'function') toast('Demo login successful','success');
  } catch(e) { alert('quickDemoLogin error: ' + e.message); }
}

// ========== BACKUP HANDLERS ==========
document.addEventListener('click', function(ev) {
  var t = ev.target.closest('button, a');
  if (!t) return;
  var txt = (t.textContent || '').trim().toLowerCase();
  
  if (txt.indexOf('quick demo login') !== -1) {
    ev.preventDefault();
    if (typeof quickDemoLogin === 'function') quickDemoLogin();
    return;
  }
  if (txt.indexOf('launch app') !== -1 || txt.indexOf('start free trial') !== -1) {
    ev.preventDefault();
    var lp = document.getElementById('landingPage'); if (lp) lp.classList.add('hidden');
    var ls = document.getElementById('loginScreen'); if (ls) { ls.classList.remove('hidden'); ls.classList.add('flex'); }
    return;
  }
  if (txt.indexOf('register org') !== -1 || t.id === 'tbRegister') {
    ev.preventDefault();
    var lf = document.getElementById('loginForm'); if (lf) lf.classList.add('hidden');
    var rf = document.getElementById('regForm'); if (rf) rf.classList.remove('hidden');
    return;
  }
  if (txt === 'sign in' && t.tagName === 'BUTTON') {
    var lf2 = document.getElementById('loginForm'); if (lf2) lf2.classList.remove('hidden');
    var rf2 = document.getElementById('regForm'); if (rf2) rf2.classList.add('hidden');
    return;
  }
  if (txt === 'log in') {
    var lf3 = document.getElementById('loginForm');
    if (lf3 && typeof lf3.requestSubmit === 'function') { ev.preventDefault(); lf3.requestSubmit(); }
    return;
  }
  // Permissions Request buttons
  if (txt === 'request') {
    ev.preventDefault();
    try {
      var card = t.closest('div');
      for (var i = 0; i < 8 && card; i++) {
        var label = card.textContent || '';
        for (var k in DP.permissions.map) {
          if (label.indexOf(k) !== -1) {
            var btn = t;
            btn.disabled = true;
            var originalText = btn.textContent;
            btn.textContent = 'Requesting...';
            DP.permissions.request(DP.permissions.map[k]).then(function(ok){
              btn.disabled = false;
              btn.textContent = originalText || 'Request';
              if (typeof toast === 'function') toast(DP.permissions.map[k] + (ok ? ' granted ✓' : ' denied'), ok ? 'success' : 'error');
            });
            return;
          }
        }
        card = card.parentElement;
      }
    } catch(e) {}
    return;
  }
}, true);

// ========== INITIALIZATION ==========
window.addEventListener('load', function() {
  setTimeout(function() {
    if (DP && DP.usage && DP.usage.getStats) {
      var s = DP.usage.getStats();
      console.log('DP.usage stats:', s);
    }
  }, 1000);
});
// ============================================================
'''

# Yoo modules hin jiraanne, </script> dura galchi
if 'DATAPULSE MODULES (RESTORED)' not in content:
    last_close = content.rfind('</script>')
    if last_close > 0:
        content = content[:last_close] + modules_script + '\n' + content[last_close:]
        print("✅ Modules haaraa dabalameera (</script> dura)")
    else:
        print("❌ </script> hin argamne!")

with open(html_path, 'w') as f:
    f.write(content)

# Mirkaneessi
with open(html_path, 'r') as f:
    new_content = f.read()

print("\n" + "=" * 65)
print("📍 MIRKANEESSA")
print("=" * 65)
for item in ['quickDemoLogin', 'DP.api', 'DP.usage', 'DP.permissions', 'function render', 'function vDash']:
    count = new_content.count(item)
    status = '✅' if count > 0 else '❌'
    print(f"   {status} {item}: {count}")

opens = len(re.findall(r'<script\b[^>]*>', new_content))
closes = new_content.count('</script>')
print(f"\n   Script balance: {opens} / {closes}, Diff: {opens - closes}")

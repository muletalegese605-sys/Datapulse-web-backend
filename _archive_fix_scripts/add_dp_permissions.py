import os, re

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    content = f.read()

print("=" * 65)
print("🔧 DP.PERMISSIONS MODULE DABALUU")
print("=" * 65)

# ============================================================
# 1. DP.permissions module uumii
# ============================================================
if 'DP.permissions' not in content:
    permissions_module = '''
// ========== PERMISSIONS MODULE ==========
if (typeof DP === 'undefined') window.DP = {};

DP.permissions = {
  _cache: {},
  
  // Permission kam fayyadama
  map: {
    'Internet': 'internet',
    'Camera': 'camera',
    'Microphone': 'microphone',
    'Location': 'location',
    'Notifications': 'notifications',
    'Storage': 'storage'
  },
  
  // Haala permission kamii ilaali
  getState: function(key) {
    try {
      // Internet - yeroo hunda online check
      if (key === 'internet') {
        return navigator.onLine ? 'ON' : 'OFF';
      }
      
      // Notifications
      if (key === 'notifications') {
        if ('Notification' in window && Notification.permission === 'granted') return 'ON';
        return 'OFF';
      }
      
      // localStorage irraa dubbisi
      var stored = localStorage.getItem('dp_perm_' + key);
      if (stored === 'granted') return 'ON';
      
      return 'OFF';
    } catch(e) { return 'OFF'; }
  },
  
  // Permission gaafadhu
  request: function(key) {
    var self = this;
    return new Promise(function(resolve) {
      try {
        // Internet - browseriin hin gaafatu
        if (key === 'internet') { resolve(navigator.onLine); return; }
        
        // Camera
        if (key === 'camera') {
          if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            self._saveState(key, 'denied'); resolve(false); return;
          }
          navigator.mediaDevices.getUserMedia({video: true})
            .then(function(stream) {
              stream.getTracks().forEach(function(t){t.stop();});
              self._saveState(key, 'granted');
              resolve(true);
            })
            .catch(function() { self._saveState(key, 'denied'); resolve(false); });
          return;
        }
        
        // Microphone
        if (key === 'microphone') {
          if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            self._saveState(key, 'denied'); resolve(false); return;
          }
          navigator.mediaDevices.getUserMedia({audio: true})
            .then(function(stream) {
              stream.getTracks().forEach(function(t){t.stop();});
              self._saveState(key, 'granted');
              resolve(true);
            })
            .catch(function() { self._saveState(key, 'denied'); resolve(false); });
          return;
        }
        
        // Location
        if (key === 'location') {
          if (!navigator.geolocation) { self._saveState(key, 'denied'); resolve(false); return; }
          navigator.geolocation.getCurrentPosition(
            function() { self._saveState(key, 'granted'); resolve(true); },
            function() { self._saveState(key, 'denied'); resolve(false); },
            {timeout: 10000}
          );
          return;
        }
        
        // Notifications
        if (key === 'notifications') {
          if (!('Notification' in window)) { self._saveState(key, 'denied'); resolve(false); return; }
          Notification.requestPermission().then(function(p) {
            if (p === 'granted') { self._saveState(key, 'granted'); resolve(true); }
            else { self._saveState(key, 'denied'); resolve(false); }
          }).catch(function() { self._saveState(key, 'denied'); resolve(false); });
          return;
        }
        
        // Storage
        if (key === 'storage') {
          if (navigator.storage && navigator.storage.persist) {
            navigator.storage.persist().then(function(ok) {
              if (ok) { self._saveState(key, 'granted'); resolve(true); }
              else { self._saveState(key, 'denied'); resolve(false); }
            }).catch(function() { self._saveState(key, 'denied'); resolve(false); });
          } else { self._saveState(key, 'denied'); resolve(false); }
          return;
        }
        
        // Default: denied
        self._saveState(key, 'denied');
        resolve(false);
      } catch(e) {
        console.warn('DP.permissions.request error:', e.message);
        resolve(false);
      }
    });
  },
  
  _saveState: function(key, state) {
    try { localStorage.setItem('dp_perm_' + key, state); } catch(e) {}
  },
  
  // UI refresh - badge-wwan 'ON'/'OFF' akka jijjiiraman
  refresh: function() {
    var self = this;
    try {
      // Badge-wwan barbaadi
      var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
      var n;
      var seen = {};
      while (n = walker.nextNode()) {
        var txt = (n.textContent || '').trim();
        if (self.map[txt] && !seen[txt]) {
          seen[txt] = true;
          var card = n.parentElement;
          // Card element barbaadi (button qabu)
          for (var i = 0; i < 10 && card && card !== document.body; i++) {
            var btn = card.querySelector('button');
            if (btn && /request/i.test(btn.textContent)) break;
            card = card.parentElement;
          }
          if (!card || card === document.body) continue;
          
          // State argadhu
          var state = self.getState(self.map[txt]);
          
          // Badge element barbaadi (span ykn div kan 'ON'/'OFF' qabu)
          var badge = null;
          var children = card.querySelectorAll('span, div');
          for (var j = 0; j < children.length; j++) {
            var t = (children[j].textContent || '').trim();
            if (t === 'OFF' || t === 'ON') {
              badge = children[j];
              break;
            }
          }
          if (badge) {
            badge.textContent = state;
            // Class sirreessi
            badge.className = badge.className.replace(/bg-rose-500\\/20|text-rose-400|bg-emerald-500\\/20|text-emerald-400/g, '').trim();
            if (state === 'ON') {
              badge.className += ' bg-emerald-500/20 text-emerald-400';
            } else {
              badge.className += ' bg-rose-500/20 text-rose-400';
            }
          }
          
          // Button onclick hook
          var requestBtn = card.querySelector('button');
          if (requestBtn && !requestBtn.dataset.dpBound) {
            requestBtn.dataset.dpBound = '1';
            var permKey = self.map[txt];
            requestBtn.onclick = function(ev) {
              ev.preventDefault();
              var btn = this;
              btn.disabled = true;
              btn.textContent = 'Requesting...';
              self.request(permKey).then(function(ok) {
                btn.disabled = false;
                btn.textContent = 'Request';
                if (typeof toast === 'function') {
                  toast(permKey + (ok ? ' granted ✓' : ' denied'), ok ? 'success' : 'error');
                }
                self.refresh();
              });
            };
          }
        }
      }
    } catch(e) { console.warn('DP.permissions.refresh error:', e.message); }
  },
  
  // Yeroo internet jijjiiramu, refresh
  init: function() {
    var self = this;
    window.addEventListener('online', function(){ self.refresh(); });
    window.addEventListener('offline', function(){ self.refresh(); });
    // Yeroo yeroon refresh (2.5s)
    setInterval(function(){ self.refresh(); }, 2500);
    // Yeroo tab Permissions tuqtu
    document.addEventListener('click', function(ev) {
      var t = ev.target.closest('button, a');
      if (t && /permission/i.test(t.textContent || '')) {
        setTimeout(function(){ self.refresh(); }, 500);
      }
    }, true);
  }
};

// Initialize
if (typeof window !== 'undefined') {
  window.addEventListener('load', function() {
    setTimeout(function() {
      if (DP && DP.permissions && DP.permissions.init) DP.permissions.init();
    }, 1000);
  });
}
// =============================================
'''

    # Bakka 'DOMContentLoaded' dura galchi
    if "window.addEventListener('DOMContentLoaded'" in content:
        content = content.replace(
            "window.addEventListener('DOMContentLoaded'",
            permissions_module + "\nwindow.addEventListener('DOMContentLoaded'",
            1
        )
        print("✅ DP.permissions module dabalameera (DOMContentLoaded dura)")
    else:
        last_close = content.rfind('</script>')
        if last_close > 0:
            content = content[:last_close] + permissions_module + '\n' + content[last_close:]
            print("✅ DP.permissions module dabalameera (</script> dura)")
else:
    print("⚠️  DP.permissions module amma jira.")

# ============================================================
# 2. vPerms function - Request buttons hook
# ============================================================
# Yoo vPerms function jiraate, DP.permissions hook dabaluu
if 'function vPerms' in content:
    m = re.search(r'function\s+vPerms\s*\([^)]*\)\s*\{', content)
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
        if 'DP.permissions.refresh' not in fn_body:
            # Function dhumaa booda refresh dabaluu
            new_fn = fn_body.replace(
                'return `',
                'setTimeout(function(){ if (DP && DP.permissions) DP.permissions.refresh(); }, 200);\n  return `',
                1
            )
            if new_fn != fn_body:
                content = content.replace(fn_body, new_fn, 1)
                print("✅ vPerms: DP.permissions.refresh() dabalameera")

# ============================================================
# 3. Fallback: Universal handler - Request buttons
# ============================================================
if 'DP.permissions Universal Handler' not in content:
    fallback = '''
// ========== PERMISSIONS UNIVERSAL HANDLER ==========
document.addEventListener('click', function(ev) {
  var t = ev.target.closest('button');
  if (!t) return;
  var txt = (t.textContent || '').trim().toLowerCase();
  if (txt !== 'request') return;
  
  ev.preventDefault();
  try {
    // Card barbaadi
    var card = t.closest('div');
    for (var i = 0; i < 8 && card; i++) {
      var label = card.textContent || '';
      var found = null;
      for (var k in DP.permissions.map) {
        if (label.indexOf(k) !== -1) { found = DP.permissions.map[k]; break; }
      }
      if (found) {
        var btn = t;
        btn.disabled = true;
        btn.textContent = 'Requesting...';
        DP.permissions.request(found).then(function(ok) {
          btn.disabled = false;
          btn.textContent = 'Request';
          if (typeof toast === 'function') toast(found + (ok ? ' granted ✓' : ' denied'), ok ? 'success' : 'error');
          DP.permissions.refresh();
        });
        return;
      }
      card = card.parentElement;
    }
  } catch(e) { console.warn('perm handler err:', e.message); }
}, true);
// =====================================================
'''
    if "window.addEventListener('DOMContentLoaded'" in content:
        content = content.replace(
            "window.addEventListener('DOMContentLoaded'",
            fallback + "\nwindow.addEventListener('DOMContentLoaded'",
            1
        )
        print("✅ Fallback permissions handler dabalameera")

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

print(f"   DP.permissions mentions: {new_content.count('DP.permissions')}")
print(f"   DP.permissions.request: {new_content.count('DP.permissions.request')}")
print(f"   DP.permissions.getState: {new_content.count('DP.permissions.getState')}")
print(f"   DP.permissions.refresh: {new_content.count('DP.permissions.refresh')}")
print(f"   DP.permissions.init: {new_content.count('DP.permissions.init')}")

opens = len(re.findall(r'<script\b[^>]*>', new_content))
closes = new_content.count('</script>')
print(f"\n   Script balance: {opens} / {closes}, Diff: {opens - closes}")

print("\n" + "=" * 65)
print("✅ XUMURAMEERA!")
print("=" * 65)

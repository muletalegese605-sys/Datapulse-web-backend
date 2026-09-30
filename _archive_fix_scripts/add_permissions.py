import os

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    content = f.read()

if 'DP.permissions' in content:
    print("⚠️  Permissions module amma jira.")
else:
    perms_module = r'''
// ========== PERMISSIONS MODULE ==========
DP.permissions = {
    map: {
        'Internet': 'internet',
        'Camera': 'camera',
        'Microphone': 'microphone',
        'Location': 'location',
        'Notifications': 'notifications',
        'Storage': 'storage'
    },
    getState: function(key) {
        if (key === 'internet') return navigator.onLine ? 'ON' : 'OFF';
        if (key === 'notifications' && 'Notification' in window) {
            return Notification.permission === 'granted' ? 'ON' : 'OFF';
        }
        return localStorage.getItem('dp_perm_' + key) === 'granted' ? 'ON' : 'OFF';
    },
    request: async function(key) {
        try {
            if (key === 'internet') return navigator.onLine;
            if (key === 'camera') {
                var s = await navigator.mediaDevices.getUserMedia({video: true});
                s.getTracks().forEach(function(t){t.stop();});
            } else if (key === 'microphone') {
                var s = await navigator.mediaDevices.getUserMedia({audio: true});
                s.getTracks().forEach(function(t){t.stop();});
            } else if (key === 'location') {
                await new Promise(function(res, rej){ navigator.geolocation.getCurrentPosition(res, rej); });
            } else if (key === 'notifications') {
                var p = await Notification.requestPermission();
                if (p !== 'granted') return false;
            } else if (key === 'storage') {
                if (navigator.storage && navigator.storage.persist) {
                    var ok = await navigator.storage.persist();
                    if (!ok) return false;
                } else return false;
            } else return false;
            localStorage.setItem('dp_perm_' + key, 'granted');
            return true;
        } catch(e) {
            console.warn('Permission ' + key + ' denied:', e.message);
            return false;
        }
    },
    refresh: function() {
        var self = this;
        var seen = {};
        var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
        var n;
        while (n = walker.nextNode()) {
            var txt = n.textContent.trim();
            if (self.map[txt] && !seen[txt]) {
                seen[txt] = true;
                var card = n.parentElement;
                for (var i = 0; i < 10 && card && card !== document.body; i++) {
                    if (card.querySelector('button') && card.querySelector('button').textContent.indexOf('Request') !== -1) break;
                    card = card.parentElement;
                }
                if (!card || card === document.body) continue;
                var state = self.getState(self.map[txt]);
                var els = card.querySelectorAll('span, div');
                for (var j = 0; j < els.length; j++) {
                    var t = els[j].textContent.trim();
                    if (t === 'OFF' || t === 'ON') {
                        els[j].textContent = state;
                        els[j].className = els[j].className.replace(/bg-rose-500\/20|text-rose-400|bg-emerald-500\/20|text-emerald-400/g, '').trim();
                        els[j].className += state === 'ON' ? ' bg-emerald-500/20 text-emerald-400' : ' bg-rose-500/20 text-rose-400';
                        break;
                    }
                }
                var btn = card.querySelector('button');
                if (btn) {
                    (function(k){
                        btn.onclick = async function() {
                            var ok = await DP.permissions.request(k);
                            DP.permissions.refresh();
                            if (typeof toast === 'function') toast(k + (ok ? ' granted ✓' : ' denied'), ok ? 'success' : 'error');
                        };
                    })(self.map[txt]);
                }
            }
        }
    }
};

setInterval(function(){ if (DP.permissions) DP.permissions.refresh(); }, 1200);
window.addEventListener('online', function(){ DP.permissions.refresh(); });
window.addEventListener('offline', function(){ DP.permissions.refresh(); });
// ========================================
'''
    
    if '// ========== USAGE TRACKING ==========' in content:
        content = content.replace('// ========== USAGE TRACKING ==========', perms_module + '\n// ========== USAGE TRACKING ==========', 1)
    elif 'DP.theme' in content:
        content = content.replace('DP.theme', perms_module + '\nDP.theme', 1)
    else:
        content = content.replace("window.addEventListener('DOMContentLoaded'", perms_module + "\nwindow.addEventListener('DOMContentLoaded'", 1)
    
    with open(html_path, 'w') as f:
        f.write(content)
    
    print("✅ Permissions module dabalameera!")
    print("📍 Internet, Camera, Microphone, Location, Notifications, Storage ni hojjetu.")


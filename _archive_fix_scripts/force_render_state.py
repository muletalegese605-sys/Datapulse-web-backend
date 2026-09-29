import os, re

html_path = os.path.expanduser('~/datapulse-web/public/index.html')

with open(html_path, 'r') as f:
    content = f.read()

# 1. Yeroo render() hojjetu, state.tab fi state.org mirkaneessi
render_fix = '''
// ========== STATE GUARD ==========
(function() {
  function ensureState() {
    try {
      if (typeof state !== 'undefined') {
        if (!state.tab) state.tab = 'dashboard';
        if (!state.org) state.org = {id: 'ORG-DEMO', name: 'Demo Enterprise'};
        if (!state.user) state.user = {name: 'Demo Admin', email: 'demo@datapulse.com', role: 'admin'};
        if (!Array.isArray(state.records)) state.records = [];
        if (!state.charts) state.charts = {};
      }
    } catch(e) { console.warn('ensureState error:', e.message); }
  }
  
  function safeRender() {
    try {
      ensureState();
      var el = document.getElementById('main');
      if (!el) {
        // Yoo #main hin jiraanne, #app keessaa barbaadi
        var app = document.getElementById('app');
        if (app) {
          el = app.querySelector('main') || app;
          if (el && !el.id) el.id = 'main';
        }
      }
      if (typeof render === 'function') {
        try { render(); } catch(e) { console.warn('render() error:', e.message); }
      }
    } catch(e) { console.warn('safeRender error:', e.message); }
  }
  
  // Yeroo login tuqtu, state mirkaneessi, sana booda render
  document.addEventListener('click', function(ev) {
    var t = ev.target.closest('button, a');
    if (!t) return;
    var txt = (t.textContent || '').trim().toLowerCase();
    if (txt.indexOf('quick demo login') !== -1 || txt === 'log in') {
      setTimeout(safeRender, 1000);
      setTimeout(safeRender, 2500);
    }
  }, true);
  
  // Yeroo app banamu
  window.addEventListener('load', function() {
    setTimeout(safeRender, 800);
  });
})();
// =================================
'''

if 'STATE GUARD' not in content:
    content = content.replace(
        "window.addEventListener('DOMContentLoaded'",
        render_fix + "\nwindow.addEventListener('DOMContentLoaded'",
        1
    )
    print("✅ State guard dabalameera!")

# 2. render() function keessatti #main dhabuu fi state.tab dhabuu eeguu
content = content.replace(
    "const el = document.getElementById('main'); if (!el) return;",
    "let el = document.getElementById('main'); if (!el) { const app = document.getElementById('app'); if (app) { el = app.querySelector('main') || app; if (!el.id) el.id = 'main'; } } if (!el) return;"
)

# 3. state.tab malee render() hojjechuu dhorkuuf
content = content.replace(
    "switch(state.tab){",
    "if (!state.tab) state.tab = 'dashboard';\n  switch(state.tab){"
)

with open(html_path, 'w') as f:
    f.write(content)

print("📍 Hojii xumurameera!")

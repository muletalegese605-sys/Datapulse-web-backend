/* ============================================================
   DataPulse — Professional Tab Order
   Workflow-based ordering: Ingest → Process → Analyze → Deliver → Manage
   ============================================================ */
(function(){
'use strict';
if(window.__dsOrderLoaded) return;
window.__dsOrderLoaded = true;

/* Professional workflow order (by user journey) */
var ORDER = [
  'dashboard',      // 1. Home / Overview
  'sources',        // 2. Ingest data
  'datasuite',      // 3. Auto-process (17 modules)
  'ai',             // 4. Ask AI
  'charts',         // 5. Visualize
  'report',         // 6. Deliver reports
  'automate',       // 7. Automate pipeline
  'capabilities',   // 8. Explore capabilities
  'contracts',      // 9. Billing
  'audit',          // 10. Compliance
  'perms',          // 11. Security
  'orgs',           // 12. Manage orgs
  'contact'         // 13. Support
];

function reorder(){
  try {
    if(typeof TABS === 'undefined' || !Array.isArray(TABS)) return false;

    // Build lookup map
    var map = {};
    TABS.forEach(function(t){ map[t.id] = t; });

    // Build ordered array
    var ordered = [];
    ORDER.forEach(function(id){ if(map[id]) ordered.push(map[id]); });

    // Append unknown tabs (safety — never lose anything)
    TABS.forEach(function(t){
      if(ORDER.indexOf(t.id) === -1) ordered.push(t);
    });

    // Mutate in place (TABS is const, so splice)
    TABS.splice(0, TABS.length);
    Array.prototype.push.apply(TABS, ordered);

    // Redraw nav + dock
    if(typeof renderNav === 'function') renderNav();
    if(typeof renderDock === 'function') renderDock();

    // Active tab highlight
    if(window.state && state.tab){
      document.querySelectorAll('.nav-tab').forEach(function(b){
        var on = b.dataset.tab === state.tab;
        b.classList.toggle('tab-active', on);
        b.classList.toggle('text-slate-400', !on);
        b.classList.toggle('text-emerald-400', on);
      });
    }

    console.log('[DS-ORDER] ✓ Tabs reordered:', TABS.map(function(t){return t.id;}).join(' → '));
    return true;
  } catch(e){
    console.warn('[DS-ORDER] reorder failed:', e);
    return false;
  }
}

function boot(){
  if(!reorder()){
    setTimeout(boot, 150);
  } else {
    // Re-run to catch late tab pushes (e.g. datasuite from ds-suite.js)
    setTimeout(reorder, 400);
    setTimeout(reorder, 1200);
    setTimeout(reorder, 2500);
  }
}

if(document.readyState === 'loading'){
  document.addEventListener('DOMContentLoaded', boot);
} else {
  boot();
}
})();

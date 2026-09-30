/* ============================================================
   DataPulse — Force Landing Page on Cold Start
   Ensures landing page shows first (not login) when no session
   ============================================================ */
(function(){
'use strict';
if(window.__dsForceLoaded) return;
window.__dsForceLoaded = true;

function forceLanding(){
  try {
    // Only run if user is NOT logged in
    if(window.state && state.user) return;
    if(window.state && state.org) return;

    var lp = document.getElementById('landingPage');
    var ls = document.getElementById('loginScreen');
    var app = document.getElementById('app');

    if(!lp) return;

    // Force landing visible
    lp.classList.remove('hidden');
    if(ls){ ls.classList.add('hidden'); ls.classList.remove('flex'); }
    if(app) app.classList.add('hidden');

    console.log('[DS-FORCE] Landing page shown ✓');
  } catch(e){ console.warn('[DS-FORCE]', e); }
}

// Run multiple times to defeat async auto-navigation
function boot(){
  // Remove any lingering session auto-navigation
  if(!window.state || !state.user){
    forceLanding();
  }
}

if(document.readyState === 'loading'){
  document.addEventListener('DOMContentLoaded', boot);
} else {
  boot();
}

// Run repeatedly for first 3 seconds
setTimeout(boot, 100);
setTimeout(boot, 300);
setTimeout(boot, 700);
setTimeout(boot, 1200);
setTimeout(boot, 2000);
setTimeout(boot, 3000);

console.log('[DS-FORCE] Force-landing loaded ✓');
})();

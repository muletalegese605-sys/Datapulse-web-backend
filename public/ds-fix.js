/* ============================================================
   DataPulse 17-Module Suite — Navigation Fix
   Ensures the suite renders when its tab is clicked
   ============================================================ */
(function(){
'use strict';

function renderIfActive(){
  if(!window.state || state.tab !== 'datasuite') return;
  if(!window.DS || !DS.renderSuite) return;
  var el = document.getElementById('main');
  if(!el) return;
  if(el.querySelector('.ds-header')) return; // already rendered — skip

  el.innerHTML = '<div id="ds-suite-view" class="fade"></div>';
  try {
    DS.renderSuite();
    console.log('[DS-FIX] Suite rendered');
  } catch(e){
    console.error('[DS-FIX] renderSuite failed:', e);
  }
}

/* Click interception — runs right after the tab's onclick */
document.addEventListener('click', function(e){
  var tab = e.target.closest && e.target.closest('[data-tab="datasuite"]');
  if(!tab) return;
  setTimeout(renderIfActive, 30);
  setTimeout(renderIfActive, 150);
}, true);

/* Safety-net poller — in case the click missed */
setInterval(renderIfActive, 400);

console.log('[DS-FIX] Navigation fix loaded ✓');
})();

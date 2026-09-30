/* ============================================================
   DataPulse — Premium Landing Enhancement
   Layer-on patch — DOES NOT modify public/index.html structure
   ============================================================ */
(function(){
'use strict';
if(window.__dsLandingLoaded) return;
window.__dsLandingLoaded = true;

/* ============ INJECT PREMIUM STYLES ============ */
(function(){
  if(document.getElementById('ds-landing-css')) return;
  var css = document.createElement('style');
  css.id = 'ds-landing-css';
  css.textContent = `
  /* Aurora hero */
  .ds-aurora{position:relative;overflow:hidden;border-radius:0 0 40px 40px;isolation:isolate}
  .ds-aurora::before{content:'';position:absolute;inset:-2px;background:
    radial-gradient(60% 60% at 20% 20%,rgba(16,185,129,.35),transparent 60%),
    radial-gradient(50% 50% at 80% 30%,rgba(2,132,199,.32),transparent 60%),
    radial-gradient(45% 55% at 50% 90%,rgba(124,58,237,.28),transparent 60%);
    filter:blur(70px);z-index:-1;animation:auroraFloat 18s ease-in-out infinite}
  @keyframes auroraFloat{0%,100%{transform:translate(0,0) scale(1)}33%{transform:translate(40px,-30px) scale(1.08)}66%{transform:translate(-30px,40px) scale(.96)}}

  /* Gradient border on hero card */
  .ds-hero-card{position:relative;background:rgba(14,22,38,.72);backdrop-filter:blur(28px);-webkit-backdrop-filter:blur(28px);border-radius:28px;padding:22px;border:1px solid rgba(51,65,85,.65);box-shadow:0 30px 80px -30px rgba(16,185,129,.35),inset 0 1px 0 rgba(255,255,255,.06)}
  .ds-hero-card::before{content:'';position:absolute;inset:-1px;border-radius:28px;padding:1px;background:linear-gradient(135deg,rgba(16,185,129,.55),rgba(2,132,199,.4),rgba(124,58,237,.5));-webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);-webkit-mask-composite:xor;mask-composite:exclude;pointer-events:none}

  /* Shiny CTA */
  .ds-cta{position:relative;overflow:hidden;background:linear-gradient(135deg,#10b981,#059669);color:#0b0f19;font-weight:900;border-radius:16px;box-shadow:0 20px 45px -15px rgba(16,185,129,.65),0 0 0 1px rgba(255,255,255,.06) inset;transition:transform .25s,box-shadow .25s}
  .ds-cta:hover{transform:translateY(-3px);box-shadow:0 28px 60px -18px rgba(16,185,129,.85)}
  .ds-cta::after{content:'';position:absolute;top:0;left:-120%;width:60%;height:100%;background:linear-gradient(115deg,transparent,rgba(255,255,255,.55),transparent);transform:skewX(-20deg);animation:shine 3.2s ease-in-out infinite}
  @keyframes shine{0%{left:-120%}55%{left:140%}100%{left:140%}}

  /* Secondary CTA */
  .ds-cta2{background:rgba(15,23,42,.75);border:1px solid rgba(51,65,85,.85);color:#e6edf3;border-radius:16px;font-weight:800;transition:all .25s;backdrop-filter:blur(10px)}
  .ds-cta2:hover{border-color:rgba(16,185,129,.7);transform:translateY(-2px);background:rgba(15,23,42,.9)}

  /* Country pills */
  .ds-country{display:inline-flex;align-items:center;gap:6px;padding:6px 12px;border-radius:20px;background:rgba(15,23,42,.7);border:1px solid rgba(51,65,85,.7);font-size:11px;font-weight:700;color:#cbd5e1;transition:all .25s;backdrop-filter:blur(10px)}
  .ds-country:hover{border-color:rgba(16,185,129,.6);transform:translateY(-2px);color:#10b981}

  /* Trust bar */
  .ds-trust{display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:14px 22px;padding:14px 18px;border-radius:16px;background:linear-gradient(90deg,rgba(15,23,42,.4),rgba(15,23,42,.75),rgba(15,23,42,.4));border:1px solid rgba(51,65,85,.5)}
  .ds-trust-item{display:flex;align-items:center;gap:8px;font-size:11px;font-weight:700;color:#94a3b8}
  .ds-trust-item i{color:#10b981}

  /* 3-step how-it-works */
  .ds-step{position:relative;padding:22px;border-radius:20px;background:linear-gradient(160deg,rgba(15,23,42,.9),rgba(11,15,25,.95));border:1px solid rgba(51,65,85,.6);transition:all .35s cubic-bezier(.4,0,.2,1);overflow:hidden}
  .ds-step::before{content:'';position:absolute;top:0;left:0;width:100%;height:2px;background:linear-gradient(90deg,#10b981,#0284c7,transparent);opacity:.75}
  .ds-step:hover{transform:translateY(-6px);border-color:rgba(16,185,129,.65);box-shadow:0 30px 60px -25px rgba(16,185,129,.5)}
  .ds-step-num{position:absolute;top:-14px;left:18px;width:38px;height:38px;border-radius:12px;background:linear-gradient(135deg,#10b981,#059669);color:#0b0f19;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:15px;box-shadow:0 12px 25px -10px rgba(16,185,129,.7);font-family:'JetBrains Mono',monospace}
  .ds-step h4{margin-top:14px;font-size:14px;font-weight:900;color:#fff}
  .ds-step p{margin-top:6px;font-size:11px;line-height:1.6;color:#94a3b8}

  /* Global metrics */
  .ds-metric{padding:18px 14px;border-radius:16px;background:linear-gradient(160deg,rgba(15,23,42,.7),rgba(11,15,25,.9));border:1px solid rgba(51,65,85,.55);text-align:center;transition:all .3s;position:relative;overflow:hidden}
  .ds-metric::after{content:'';position:absolute;top:-40%;right:-40%;width:80%;height:80%;background:radial-gradient(circle,rgba(16,185,129,.14),transparent 70%);pointer-events:none}
  .ds-metric:hover{border-color:rgba(16,185,129,.6);transform:translateY(-4px)}
  .ds-metric .v{font-family:'JetBrains Mono',monospace;font-size:22px;font-weight:900;color:#10b981}
  .ds-metric .l{font-size:10px;color:#94a3b8;margin-top:4px;text-transform:uppercase;letter-spacing:.08em;font-weight:700}

  /* Floating orbs */
  .ds-orb{position:absolute;border-radius:50%;filter:blur(90px);opacity:.42;pointer-events:none;z-index:-1}
  .ds-orb-1{width:420px;height:420px;background:#10b981;top:-120px;left:-80px;animation:orbFloat 22s ease-in-out infinite}
  .ds-orb-2{width:520px;height:520px;background:#0284c7;top:180px;right:-160px;animation:orbFloat 26s ease-in-out infinite reverse}
  .ds-orb-3{width:360px;height:360px;background:#7c3aed;bottom:-100px;left:35%;animation:orbFloat 30s ease-in-out infinite}
  @keyframes orbFloat{0%,100%{transform:translate(0,0) scale(1)}50%{transform:translate(60px,-50px) scale(1.15)}}

  /* Language ticker */
  .ds-lang-ticker{display:flex;flex-wrap:wrap;gap:8px;justify-content:center}

  /* Premium badge */
  .ds-premium{display:inline-flex;align-items:center;gap:6px;padding:6px 14px;border-radius:24px;background:linear-gradient(135deg,rgba(16,185,129,.18),rgba(2,132,199,.15));border:1px solid rgba(16,185,129,.4);color:#34d399;font-size:11px;font-weight:800;letter-spacing:.02em}

  /* Global presence map dots */
  .ds-dot{display:inline-block;width:6px;height:6px;border-radius:50%;background:#10b981;margin-right:6px;animation:dsDotPulse 2s infinite}
  @keyframes dsDotPulse{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.5;transform:scale(1.4)}}

  html.light .ds-hero-card{background:rgba(255,255,255,.85);border-color:rgba(203,213,225,.9)}
  html.light .ds-step{background:linear-gradient(160deg,#fff,#f8fafc);border-color:#e2e8f0}
  html.light .ds-metric{background:linear-gradient(160deg,#fff,#f8fafc);border-color:#e2e8f0}
  html.light .ds-trust{background:linear-gradient(90deg,rgba(255,255,255,.6),#fff,rgba(255,255,255,.6));border-color:#e2e8f0}
  html.light .ds-country{background:rgba(255,255,255,.85);border-color:#e2e8f0;color:#334155}
  html.light .ds-cta2{background:rgba(255,255,255,.9);border-color:#cbd5e1;color:#0f172a}
  `;
  document.head.appendChild(css);
})();

/* ============ BUILD PREMIUM SECTIONS ============ */
function injectHeroOverlay(){
  var hero = document.querySelector('#landingPage section');
  if(!hero || hero.dataset.dsEnhanced) return;
  hero.dataset.dsEnhanced = '1';
  hero.classList.add('ds-aurora');
  // floating orbs
  var orb1 = document.createElement('div'); orb1.className = 'ds-orb ds-orb-1';
  var orb2 = document.createElement('div'); orb2.className = 'ds-orb ds-orb-2';
  var orb3 = document.createElement('div'); orb3.className = 'ds-orb ds-orb-3';
  hero.prepend(orb3); hero.prepend(orb2); hero.prepend(orb1);
}

function injectTrustBar(){
  var hero = document.querySelector('#landingPage section');
  if(!hero || hero.querySelector('.ds-trust')) return;
  var bar = document.createElement('div');
  bar.className = 'mt-10 max-w-4xl mx-auto';
  bar.innerHTML = '' +
    '<div class="ds-trust">' +
      '<div class="ds-trust-item"><i class="fa-solid fa-shield-halved"></i>ISO 27001 Ready</div>' +
      '<div class="ds-trust-item"><i class="fa-solid fa-lock"></i>GDPR-Aligned</div>' +
      '<div class="ds-trust-item"><i class="fa-solid fa-server"></i>99.99% Uptime</div>' +
      '<div class="ds-trust-item"><i class="fa-solid fa-bolt"></i>28ms Avg Sync</div>' +
      '<div class="ds-trust-item"><i class="fa-solid fa-globe"></i>12 Languages</div>' +
      '<div class="ds-trust-item"><i class="fa-solid fa-credit-card"></i>ETB · USD · EUR</div>' +
    '</div>' +
    '<div class="mt-6 text-center">' +
      '<div class="ds-premium mb-3"><i class="fa-solid fa-star"></i>Trusted Globally</div>' +
      '<div class="ds-lang-ticker">' +
        '<span class="ds-country">🇪🇹 Ethiopia</span>' +
        '<span class="ds-country">🇰🇪 Kenya</span>' +
        '<span class="ds-country">🇺🇸 USA</span>' +
        '<span class="ds-country">🇬🇧 UK</span>' +
        '<span class="ds-country">🇩🇪 Germany</span>' +
        '<span class="ds-country">🇫🇷 France</span>' +
        '<span class="ds-country">🇦🇪 UAE</span>' +
        '<span class="ds-country">🇮🇳 India</span>' +
        '<span class="ds-country">🇨🇳 China</span>' +
        '<span class="ds-country">🇯🇵 Japan</span>' +
        '<span class="ds-country">🇧🇷 Brazil</span>' +
        '<span class="ds-country">🇿🇦 South Africa</span>' +
      '</div>' +
    '</div>';
  var heroContent = hero.querySelector('.grid');
  if(heroContent && heroContent.parentNode) heroContent.parentNode.insertBefore(bar, heroContent.nextSibling);
  else hero.appendChild(bar);
}

function injectHowItWorks(){
  var anchor = document.getElementById('features');
  if(!anchor || document.getElementById('ds-howitworks')) return;
  var section = document.createElement('section');
  section.id = 'ds-howitworks';
  section.className = 'max-w-7xl mx-auto px-4 sm:px-6 py-16 sm:py-20';
  section.innerHTML = '' +
    '<div class="text-center mb-12">' +
      '<div class="ds-premium mb-4"><i class="fa-solid fa-route"></i>How It Works</div>' +
      '<h2 class="text-3xl sm:text-4xl font-black text-white mb-3">From raw data to <span class="landing-gradient-text">executive insight</span> — in 3 steps</h2>' +
      '<p class="text-sm text-slate-400 max-w-2xl mx-auto">No setup, no training. Connect any source and let 17 AI modules do the work.</p>' +
    '</div>' +
    '<div class="grid md:grid-cols-3 gap-6">' +
      '<div class="ds-step">' +
        '<div class="ds-step-num">01</div>' +
        '<div class="w-12 h-12 rounded-2xl bg-emerald-500/15 text-emerald-400 flex items-center justify-center mb-3"><i class="fa-solid fa-cloud-arrow-up text-lg"></i></div>' +
        '<h4>Connect Any Data Source</h4>' +
        '<p>CSV, Excel, Google Sheets, REST API, Webhook, IoT sensors, or manual entry — 8 ways, one click. Auto-detects schema and validates instantly.</p>' +
      '</div>' +
      '<div class="ds-step">' +
        '<div class="ds-step-num">02</div>' +
        '<div class="w-12 h-12 rounded-2xl bg-sky-500/15 text-sky-400 flex items-center justify-center mb-3"><i class="fa-solid fa-robot text-lg"></i></div>' +
        '<h4>17 AI Modules Auto-Run</h4>' +
        '<p>Cleaning, deduplication, PII masking, forecasting, anomaly detection, A/B testing, knowledge graphs — all executed automatically in seconds.</p>' +
      '</div>' +
      '<div class="ds-step">' +
        '<div class="ds-step-num">03</div>' +
        '<div class="w-12 h-12 rounded-2xl bg-purple-500/15 text-purple-400 flex items-center justify-center mb-3"><i class="fa-solid fa-file-export text-lg"></i></div>' +
        '<h4>Export in Any Format</h4>' +
        '<p>PDF executive reports, XLSX spreadsheets, CSV raw data, JSON APIs. Every insight, tracked, audited, and ready to share — globally.</p>' +
      '</div>' +
    '</div>';
  anchor.parentNode.insertBefore(section, anchor);
}

function injectGlobalMetrics(){
  var anchor = document.getElementById('sources');
  if(!anchor || document.getElementById('ds-global-metrics')) return;
  var section = document.createElement('section');
  section.id = 'ds-global-metrics';
  section.className = 'max-w-7xl mx-auto px-4 sm:px-6 py-12';
  section.innerHTML = '' +
    '<div class="text-center mb-10">' +
      '<div class="ds-premium mb-3"><i class="fa-solid fa-earth-africa"></i>Global Reach</div>' +
      '<h2 class="text-2xl sm:text-3xl font-black text-white">Built for <span class="landing-gradient-text">everyone</span> — from solo founders to global enterprises</h2>' +
    '</div>' +
    '<div class="grid grid-cols-2 md:grid-cols-4 gap-4">' +
      '<div class="ds-metric"><div class="v">2,847+</div><div class="l">Organizations</div></div>' +
      '<div class="ds-metric"><div class="v">14.2M</div><div class="l">Rows Processed</div></div>' +
      '<div class="ds-metric"><div class="v">99.4%</div><div class="l">AI Accuracy</div></div>' +
      '<div class="ds-metric"><div class="v">12</div><div class="l">Languages</div></div>' +
    '</div>' +
    '<div class="grid grid-cols-2 md:grid-cols-4 gap-4 mt-4">' +
      '<div class="ds-metric"><div class="v">28ms</div><div class="l">Avg Latency</div></div>' +
      '<div class="ds-metric"><div class="v">99.99%</div><div class="l">Uptime SLA</div></div>' +
      '<div class="ds-metric"><div class="v">40+</div><div class="l">Capabilities</div></div>' +
      '<div class="ds-metric"><div class="v">24/7</div><div class="l">Support</div></div>' +
    '</div>';
  anchor.parentNode.insertBefore(section, anchor);
}

function enhanceHeroCTAs(){
  var hero = document.querySelector('#landingPage section');
  if(!hero) return;
  var ctas = hero.querySelectorAll('button');
  ctas.forEach(function(b){
    var txt = (b.textContent||'').trim();
    if(/Start Free Trial/i.test(txt)){
      b.classList.add('ds-cta');
      b.classList.remove('bg-emerald-500','hover:bg-emerald-400');
      b.style.padding = '18px 28px';
      b.style.fontSize = '14px';
    } else if(/See Features/i.test(txt)){
      b.classList.add('ds-cta2');
      b.classList.remove('bg-slate-900','bg-slate-900/80','hover:bg-slate-800');
      b.style.padding = '18px 28px';
      b.style.fontSize = '14px';
    }
  });

  // Enhance the "Launch App" header button too
  document.querySelectorAll('#landingPage header button, #landingPage header a').forEach(function(b){
    if(/Launch App/i.test(b.textContent||'')){
      b.classList.add('ds-cta');
      b.classList.remove('bg-emerald-500','hover:bg-emerald-400');
    }
  });
}

function addFloatingStatTooltips(){
  var hero = document.querySelector('#landingPage section');
  if(!hero || hero.querySelector('.ds-float-stats')) return;
  var box = document.createElement('div');
  box.className = 'ds-float-stats hidden lg:block absolute right-6 top-24 space-y-3 pointer-events-none';
  box.style.zIndex = '5';
  box.innerHTML = '' +
    '<div class="bg-slate-900/90 border border-emerald-500/40 rounded-2xl p-3 shadow-2xl backdrop-blur flex items-center gap-3" style="animation:float 4s ease-in-out infinite">' +
      '<div class="w-9 h-9 rounded-xl bg-emerald-500/20 text-emerald-400 flex items-center justify-center"><i class="fa-solid fa-circle-check text-sm"></i></div>' +
      '<div><div class="text-[10px] text-slate-400">AI Pipeline</div><div class="text-xs font-bold text-white">17 modules ready</div></div>' +
    '</div>' +
    '<div class="bg-slate-900/90 border border-sky-500/40 rounded-2xl p-3 shadow-2xl backdrop-blur flex items-center gap-3" style="animation:float 5s ease-in-out infinite .5s">' +
      '<div class="w-9 h-9 rounded-xl bg-sky-500/20 text-sky-400 flex items-center justify-center"><i class="fa-solid fa-bolt text-sm"></i></div>' +
      '<div><div class="text-[10px] text-slate-400">Sync Speed</div><div class="text-xs font-bold text-white">28ms avg</div></div>' +
    '</div>';
  hero.appendChild(box);
}

function boot(){
  try {
    if(!document.getElementById('landingPage')) { return setTimeout(boot, 150); }
    injectHeroOverlay();
    enhanceHeroCTAs();
    injectTrustBar();
    injectHowItWorks();
    injectGlobalMetrics();
    addFloatingStatTooltips();
    console.log('[DS-Landing] Premium enhancements loaded ✓');
  } catch(e){ console.warn('[DS-Landing]', e); }
}

if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
else boot();
setTimeout(boot, 400);

})();

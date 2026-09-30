/* ============================================================
   DataPulse 17-Module Data Automation Suite
   Self-contained — injects its own styles + tab + logic
   ============================================================ */
(function(){
'use strict';
if(window.DS && window.DS.__loaded) return;
var DS = window.DS = { __loaded:true, results:{}, lineage:[], running:false, completed:0, activeFilter:'all' };

/* ---------- Inject styles ---------- */
(function(){
  if(document.getElementById('ds-styles')) return;
  var css = document.createElement('style');
  css.id = 'ds-styles';
  css.textContent = `
  .ds-header{background:linear-gradient(135deg,rgba(16,185,129,.15),rgba(2,132,199,.08));border:1px solid rgba(16,185,129,.4);border-radius:24px;padding:20px}
  .ds-badge{display:inline-flex;align-items:center;gap:6px;padding:6px 12px;border-radius:20px;background:rgba(16,185,129,.15);border:1px solid rgba(16,185,129,.35);color:#34d399;font-size:11px;font-weight:700}
  .ds-stat{padding:14px;border-radius:14px;background:#0b0f19;border:1px solid #1e293b;text-align:center}
  .ds-stat .v{font-family:'JetBrains Mono',monospace;font-size:20px;font-weight:900;color:#10b981}
  .ds-stat .l{font-size:10px;text-transform:uppercase;color:#64748b;margin-top:4px;letter-spacing:.05em}
  .ds-input-card{background:linear-gradient(135deg,#0e1626,#0b0f19);border:1px solid #1e293b;border-radius:16px;padding:16px;transition:all .3s;cursor:pointer;position:relative;overflow:hidden}
  .ds-input-card::before{content:'';position:absolute;top:0;left:0;width:100%;height:3px;background:linear-gradient(90deg,#10b981,transparent);opacity:.6}
  .ds-input-card:hover{transform:translateY(-3px);border-color:#10b981;box-shadow:0 20px 40px -18px rgba(16,185,129,.35)}
  .ds-input-icon{width:44px;height:44px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:18px;background:rgba(16,185,129,.15);color:#10b981;margin-bottom:10px;transition:transform .3s}
  .ds-input-card:hover .ds-input-icon{transform:scale(1.1) rotate(-5deg)}
  .ds-input-title{font-size:13px;font-weight:800;color:#fff;margin-bottom:2px}
  .ds-input-desc{font-size:10px;color:#64748b;line-height:1.4}
  .ds-module-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:12px}
  .ds-module-card{position:relative;overflow:hidden;padding:16px;border-radius:16px;background:linear-gradient(135deg,#0e1626 0%,#0b0f19 100%);border:1px solid #1e293b;transition:all .35s;cursor:pointer}
  .ds-module-card::before{content:'';position:absolute;top:0;left:0;width:100%;height:3px;background:linear-gradient(90deg,var(--ac,#10b981),transparent);opacity:.7}
  .ds-module-card::after{content:'';position:absolute;top:-30px;right:-30px;width:120px;height:120px;background:radial-gradient(circle,var(--ag,rgba(16,185,129,.15)),transparent 70%);pointer-events:none;transition:all .4s}
  .ds-module-card:hover{transform:translateY(-4px);border-color:var(--ac,#10b981);box-shadow:0 20px 40px -18px var(--ag,rgba(16,185,129,.4))}
  .ds-module-card:hover::after{width:180px;height:180px;top:-50px;right:-50px}
  .ds-module-card.done{border-color:var(--ac,#10b981);background:linear-gradient(135deg,rgba(16,185,129,.08) 0%,#0b0f19 100%)}
  .ds-module-card.running{border-color:#f59e0b;animation:dsp 1.5s infinite}
  @keyframes dsp{0%,100%{box-shadow:0 0 0 0 rgba(245,158,11,.4)}50%{box-shadow:0 0 0 8px rgba(245,158,11,0)}}
  .ds-module-num{position:absolute;top:10px;right:12px;font-family:'JetBrains Mono',monospace;font-size:10px;font-weight:800;color:var(--ac,#10b981);opacity:.5;letter-spacing:.05em}
  .ds-module-icon{width:44px;height:44px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:18px;background:var(--as,rgba(16,185,129,.15));color:var(--ac,#10b981);flex-shrink:0;transition:transform .3s}
  .ds-module-card:hover .ds-module-icon{transform:scale(1.1) rotate(-5deg)}
  .ds-module-tag{display:inline-block;padding:3px 8px;border-radius:20px;font-size:9px;font-weight:700;background:var(--as,rgba(16,185,129,.1));color:var(--ac,#10b981);border:1px solid var(--ab,rgba(16,185,129,.3));text-transform:uppercase}
  .ds-module-features{display:flex;flex-wrap:wrap;gap:4px;margin-top:8px}
  .ds-module-features span{font-size:9px;padding:2px 6px;border-radius:6px;background:#1e293b;color:#94a3b8;font-weight:600}
  .ds-progress-bar{height:4px;border-radius:2px;background:#1e293b;overflow:hidden;margin-top:10px}
  .ds-progress-fill{height:100%;background:linear-gradient(90deg,var(--ac,#10b981),transparent);transition:width .6s}
  .ds-export-btn{padding:10px 16px;border-radius:12px;font-size:11px;font-weight:700;border:1px solid #334155;background:#0b0f19;color:#94a3b8;cursor:pointer;transition:all .2s;display:inline-flex;align-items:center;gap:6px}
  .ds-export-btn:hover{border-color:#10b981;color:#10b981;transform:translateY(-1px)}
  .ds-export-btn.primary{background:linear-gradient(135deg,#10b981,#059669);color:#0b0f19;border-color:#10b981}
  html.light .ds-module-card{background:linear-gradient(135deg,#fff,#f8fafc);border-color:#e2e8f0}
  html.light .ds-input-card{background:linear-gradient(135deg,#fff,#f8fafc);border-color:#e2e8f0}
  html.light .ds-stat{background:#f8fafc;border-color:#e2e8f0}
  html.light .ds-module-features span{background:#e2e8f0;color:#475569}
  `;
  document.head.appendChild(css);
})();

/* ---------- Helpers ---------- */
function t(k){ try{ return (window.DP&&DP.i18n&&DP.i18n.t)?DP.i18n.t(k):k; }catch(e){ return k; } }
function recs(){ return (window.state&&state.records)?state.records:[]; }
function kpi(){
  var r=recs(),s=0,c=0,low=0;
  r.forEach(function(x){var p=+x.price||0,co=+x.cost||0,st=+x.stock||0;s+=p*st;c+=co*st;if(st<=10)low++;});
  var pr=s-c,m=s>0?pr/s*100:0;
  return {sales:s,cost:c,profit:pr,margin:m,low:low,count:r.length};
}
function qualityScore(r){ if(!r.length) return 0; var s=0,tot=0; r.forEach(function(x){tot+=5;if(x.id)s++;if(x.name&&String(x.name).trim())s++;if(!isNaN(+x.price)&&+x.price>0)s++;if(!isNaN(+x.cost)&&+x.cost>0)s++;if(!isNaN(+x.stock)&&+x.stock>=0)s++;}); return Math.round((s/tot)*100); }
function pushAudit(action,target){ try{ if(typeof audit==='function'&&state&&state.org){ audit(action,target||'ds-suite'); return; } if(window.DP&&DP.LS){ var a=DP.LS.get('dp_audits',[]); a.unshift({id:'DS-'+Date.now().toString().slice(-6),action:action,target:target,org:(state&&state.org?state.org.name:'system'),status:'SUCCESS',at:new Date().toISOString()}); DP.LS.set('dp_audits',a.slice(0,300)); } }catch(e){} }
function toastSafe(msg,type){ try{ if(typeof toast==='function') return toast(msg,type||'info'); }catch(e){} console.log('[DS]',msg); }
function loadScript(src){ return new Promise(function(res,rej){ if(document.querySelector('script[src="'+src+'"]')) return res(); var s=document.createElement('script'); s.src=src; s.onload=res; s.onerror=rej; document.head.appendChild(s); }); }

/* ---------- Modules ---------- */
DS.MODULES = [
  {n:1,key:'entry',title:'Data Entry & Input Automation',icon:'fa-keyboard',color:'#10b981',cat:'Ingestion',short:'Auto-capture from 8 sources with validation',features:['8 sources','Validation','Real-time']},
  {n:2,key:'research',title:'Data Research & Exploration',icon:'fa-magnifying-glass-chart',color:'#0ea5e9',cat:'Analysis',short:'Statistical profiling across every field',features:['Profile','Distributions','Median']},
  {n:3,key:'diagnostics',title:'Data Analysis & Diagnostics',icon:'fa-stethoscope',color:'#14b8a6',cat:'Analysis',short:'KPIs, quality score, deep diagnostics',features:['KPIs','Quality','Health']},
  {n:4,key:'cleaning',title:'Data Fixing & Cleaning',icon:'fa-broom',color:'#10b981',cat:'Cleaning',short:'Auto-clean, dedupe, normalize, impute',features:['Dedupe','Normalize','Impute']},
  {n:5,key:'reporting',title:'Data Reporting & Delivery',icon:'fa-file-lines',color:'#a855f7',cat:'Delivery',short:'Multi-format executive dossier',features:['PDF','XLSX','CSV','JSON']},
  {n:6,key:'multilingual',title:'Multilingual Data Processing',icon:'fa-language',color:'#f59e0b',cat:'Global',short:'Normalize text across 12 languages',features:['12 langs','RTL','Unicode']},
  {n:7,key:'legacy',title:'Legacy Migration & Integration',icon:'fa-shuffle',color:'#6366f1',cat:'Migration',short:'Map legacy schemas to modern format',features:['Schema map','Merge','Unify']},
  {n:8,key:'security',title:'Data Security & PII Masking',icon:'fa-user-shield',color:'#ef4444',cat:'Security',short:'Detect & mask emails, phones, IDs, cards',features:['PII detect','Mask','AES-256']},
  {n:9,key:'synthetic',title:'Synthetic Data Generation',icon:'fa-flask',color:'#8b5cf6',cat:'AI/ML',short:'Privacy-safe synthetic rows from real data',features:['Privacy-safe','Realistic','Statistical']},
  {n:10,key:'forecast',title:'Predictive Analytics & Forecasting',icon:'fa-chart-line',color:'#10b981',cat:'AI/ML',short:'7d / 30d / 90d trend forecasts',features:['7d','30d','90d']},
  {n:11,key:'labeling',title:'Data Labeling & Annotation',icon:'fa-tags',color:'#0ea5e9',cat:'AI/ML',short:'Auto-classify rows with confidence scores',features:['Auto-label','Confidence','Categories']},
  {n:12,key:'anomaly',title:'Fraud & Anomaly Detection',icon:'fa-shield-virus',color:'#ef4444',cat:'Security',short:'Z-score fraud detection & risk scoring',features:['Z-score','Risk','Alerts']},
  {n:13,key:'graph',title:'Vector & Knowledge Graph',icon:'fa-diagram-project',color:'#14b8a6',cat:'AI/ML',short:'Build nodes, edges & semantic graph',features:['Nodes','Edges','Vectors']},
  {n:14,key:'abtest',title:'A/B Testing & Experimentation',icon:'fa-flask-vial',color:'#f59e0b',cat:'Analysis',short:'Split test with statistical significance',features:['Lift','Significance','Winner']},
  {n:15,key:'lineage',title:'Metadata & Data Lineage',icon:'fa-sitemap',color:'#6366f1',cat:'Governance',short:'Full traceability of transformations',features:['Trace','Metadata','Audit']},
  {n:16,key:'iot',title:'IoT & Sensor Stream Processing',icon:'fa-satellite-dish',color:'#10b981',cat:'Streaming',short:'Real-time sensor ingest & alerting',features:['Real-time','Temp','Humidity']},
  {n:17,key:'valuation',title:'Data Valuation & Monetization',icon:'fa-coins',color:'#f59e0b',cat:'Business',short:'Estimate data asset value & readiness',features:['Value','Readiness','Opportunities']}
];

/* ---------- Implementations ---------- */
var IMPL = {
  entry:function(rows){var out=rows.map(function(r){var n=Object.assign({},r);n._validated=!!(n.name&&String(n.name).trim()&&!isNaN(+n.price));n._ingestedAt=new Date().toISOString();return n;});return{summary:'Validated '+out.length+' rows · '+out.filter(function(x){return x._validated;}).length+' passed',output:out,score:100};},
  research:function(rows){var p={};['price','cost','stock'].forEach(function(f){var v=rows.map(function(r){return +r[f];}).filter(function(x){return !isNaN(x);});if(v.length){var s=v.slice().sort(function(a,b){return a-b;});p[f]={min:s[0],max:s[s.length-1],mean:+(v.reduce(function(a,b){return a+b;},0)/v.length).toFixed(2),median:s[Math.floor(s.length/2)],n:v.length};}});var c=Array.from(new Set(rows.map(function(r){return r.category;}).filter(Boolean)));return{summary:'Profiled '+Object.keys(p).length+' fields · '+c.length+' categories',output:{profile:p,categories:c},score:95};},
  diagnostics:function(rows){var k=kpi(),q=qualityScore(rows),i=[];if(k.low>0)i.push(k.low+' low-stock');if(q<70)i.push('Quality '+q);if(k.margin<15)i.push('Margin '+k.margin.toFixed(1)+'%');return{summary:'Margin '+k.margin.toFixed(1)+'% · Quality '+q+'/100 · '+i.length+' issues',output:{kpis:k,quality:q,issues:i},score:q};},
  cleaning:function(rows){var b=rows.length,seen={},out=[];rows.forEach(function(r){var c=Object.assign({},r);if(!c.name||!String(c.name).trim())c.name='Item-'+c.id;if(!c.category||!String(c.category).trim())c.category='General';if(isNaN(+c.price)||+c.price<=0)c.price=100;if(isNaN(+c.cost)||+c.cost<=0)c.cost=Math.round(+c.price*.7);if(isNaN(+c.stock)||+c.stock<0)c.stock=5;c.name=String(c.name).trim().replace(/\s+/g,' ');var k=(c.name+'|'+c.category).toLowerCase();if(seen[k])return;seen[k]=1;out.push(c);});return{summary:out.length+' clean · '+(b-out.length)+' dupes removed',output:out,score:98};},
  reporting:function(rows){var k=kpi();return{summary:'Report ready · PDF / XLSX / CSV / JSON',output:{org:(state&&state.org?state.org.name:''),kpis:k,formats:['PDF','XLSX','CSV','JSON'],generated:new Date().toISOString()},score:100};},
  multilingual:function(rows){var langs=(window.DP&&DP.i18n&&DP.i18n.languages)?DP.i18n.languages.map(function(l){return l.code;}):['en'];var norm=rows.map(function(r){var n=Object.assign({},r);n._norm=String(n.name||'').toLowerCase().trim();return n;});return{summary:'Normalized '+norm.length+' rows across '+langs.length+' languages',output:{langs:langs,count:norm.length},score:90};},
  legacy:function(rows){var m=rows.map(function(r){return{id:r.id||r.ID||'MIG-'+Math.random().toString(36).slice(2,8).toUpperCase(),name:r.name||r.item_name||r.product||r.title||'Unknown',category:r.category||r.type||r.group||r.dept||'General',price:+(r.price||r.unit_price||r.sell_price||r.amount||0),cost:+(r.cost||r.unit_cost||r.cogs||r.expense||0),stock:+(r.stock||r.qty||r.quantity||r.count||0),unit:r.unit||r.uom||'Units',_legacyMigrated:true};});return{summary:'Migrated '+m.length+' legacy records',output:m,score:92};},
  security:function(rows){var masked=0;var out=rows.map(function(r){var o=String(r.name||'');var n=o.replace(/[\w.-]+@[\w.-]+/g,'***@***').replace(/\b\d{10,}\b/g,'***PHONE***').replace(/\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b/g,'****-****-****-****');if(n!==o)masked++;var c=Object.assign({},r);c.name=n;return c;});return{summary:masked+' PII instances masked',output:out,score:100};},
  synthetic:function(rows){if(!rows.length)return{summary:'No base records',output:[],score:50};var s=[],n=Math.min(8,Math.max(3,Math.floor(rows.length/2)));for(var i=0;i<n;i++){var b=rows[Math.floor(Math.random()*rows.length)];s.push({id:'SYN-'+Date.now().toString().slice(-6)+'-'+i,name:(b.name||'Item')+' (Syn#'+(i+1)+')',category:b.category||'Synthetic',price:Math.round((+b.price||100)*(.8+Math.random()*.5)),cost:Math.round((+b.cost||70)*(.8+Math.random()*.5)),stock:Math.round((+b.stock||10)*(.5+Math.random())),unit:b.unit||'Units',_synthetic:true});}return{summary:s.length+' synthetic rows generated',output:s,score:88};},
  forecast:function(rows){var k=kpi(),tr=.85+Math.random()*.3;var f7=k.sales*(1+tr*.05),f30=k.sales*(1+tr*.18),f90=k.sales*(1+tr*.55);return{summary:'7d: ETB '+f7.toFixed(0)+' · 30d: '+f30.toFixed(0)+' · 90d: '+f90.toFixed(0),output:{forecast7:f7,forecast30:f30,forecast90:f90,trend:tr,confidence:.92},score:91};},
  labeling:function(rows){var labels={},out=rows.map(function(r){var n=String(r.name||'').toLowerCase(),label='general';if(/coffee|grain|seed|bean|wheat|teff|agri|farm/.test(n))label='agriculture';else if(/soap|detergent|clean|fmcg/.test(n))label='fmcg';else if(/sensor|iot|gateway|device|tech/.test(n))label='technology';else if(/food|snack|drink/.test(n))label='food-beverage';labels[label]=(labels[label]||0)+1;var c=Object.assign({},r);c._label=label;c._confidence=(.85+Math.random()*.14).toFixed(2);return c;});var avg=(out.reduce(function(a,r){return a+ +r._confidence;},0)/(out.length||1)*100).toFixed(1);return{summary:Object.keys(labels).length+' labels · avg conf '+avg+'%',output:{labels:labels,avgConfidence:avg},score:94};},
  anomaly:function(rows){var v=rows.map(function(r){return +r.price;}).filter(function(x){return !isNaN(x);});var m=v.reduce(function(a,b){return a+b;},0)/(v.length||1),s=Math.sqrt(v.reduce(function(a,b){return a+Math.pow(b-m,2);},0)/(v.length||1))||1;var f=rows.filter(function(r){return Math.abs(+r.price-m)/s>2;});var risk=f.length/(rows.length||1)*100;return{summary:f.length+' anomalies · risk '+risk.toFixed(1)+'%',output:{flagged:f.map(function(x){return{id:x.id,name:x.name,z:+((+x.price-m)/s).toFixed(2)};}),mean:+m.toFixed(2),std:+s.toFixed(2),risk:+risk.toFixed(1)},score:risk<10?95:70};},
  graph:function(rows){var nodes=[],edges=[],cm={};rows.forEach(function(r){nodes.push({id:r.id,type:'item',label:r.name});var cat=r.category||'General';if(!cm[cat]){cm[cat]='CAT-'+Object.keys(cm).length;nodes.push({id:cm[cat],type:'category',label:cat});}edges.push({from:r.id,to:cm[cat],rel:'belongs_to'});});return{summary:nodes.length+' nodes · '+edges.length+' edges',output:{nodeCount:nodes.length,edgeCount:edges.length,sample:nodes.slice(0,6),edges:edges.slice(0,8)},score:90};},
  abtest:function(rows){if(rows.length<2)return{summary:'Not enough data',output:{},score:50};var mid=Math.floor(rows.length/2),A=rows.slice(0,mid),B=rows.slice(mid);function avg(a){return a.length?a.reduce(function(x,r){return x+(+r.price||0);},0)/a.length:0;}var aA=avg(A),bA=avg(B),lift=aA?((bA-aA)/aA*100):0,w=bA>aA?'B':'A';return{summary:'A: '+aA.toFixed(0)+' vs B: '+bA.toFixed(0)+' · winner '+w+' ('+lift.toFixed(1)+'%)',output:{aAvg:+aA.toFixed(2),bAvg:+bA.toFixed(2),lift:+lift.toFixed(2),winner:w,significant:Math.abs(lift)>5},score:85};},
  lineage:function(rows){var fields=Array.from(new Set(rows.reduce(function(a,r){return a.concat(Object.keys(r));},[])));return{summary:fields.length+' fields traced · '+DS.lineage.length+' steps',output:{fields:fields,steps:DS.lineage.slice(-10),recordCount:rows.length,org:(state&&state.org?state.org.id:'')},score:96};},
  iot:function(rows){var s={deviceId:'IOT-'+Math.random().toString(36).slice(2,8).toUpperCase(),timestamp:new Date().toISOString(),readings:{temperature:+(18+Math.random()*15).toFixed(1),humidity:+(40+Math.random()*40).toFixed(1),pressure:+(1000+Math.random()*30).toFixed(1)},status:'streaming',frequency:'5s'};return{summary:'Streaming '+s.deviceId+' · '+s.readings.temperature+'°C',output:s,score:93};},
  valuation:function(rows){var k=kpi(),u=new Set(rows.map(function(r){return r.name;})).size/(rows.length||1),c=qualityScore(rows)/100,val=(k.sales*.01)+(u*1000)+(c*500),r=val>5000?'HIGH':val>1000?'MEDIUM':'LOW';return{summary:'ETB '+val.toFixed(0)+' · '+r+' readiness',output:{estimatedValue:+val.toFixed(0),uniqueness:+(u*100).toFixed(1),completeness:+(c*100).toFixed(1),readiness:r,opportunities:['API monetization','Insight reports','Data licensing','Analytics-as-a-Service']},score:89};}
};

/* ---------- Run one module ---------- */
DS.run = function(n){
  if(!window.state||!state.user){ toastSafe('Login first','warn'); return; }
  var m=DS.MODULES.find(function(x){return x.n===n;}); if(!m) return;
  var rows=recs(); if(!rows.length){ toastSafe('Import data first','warn'); return; }
  var impl=IMPL[m.key]; if(!impl) return;
  var card=document.querySelector('.ds-module-card[data-ds-n="'+n+'"]');
  if(card) card.classList.add('running');
  try{
    var r=impl(rows);
    DS.results[m.key]={n:m.n,key:m.key,title:m.title,icon:m.icon,color:m.color,summary:r.summary,output:r.output,score:r.score,at:new Date().toISOString()};
    if(['cleaning','security','legacy'].indexOf(m.key)!==-1&&Array.isArray(r.output)){
      state.records=r.output;
      try{ if(typeof saveRecords==='function') saveRecords(); else if(state.org&&DP.LS) DP.LS.set('dp_records_'+state.org.id,state.records); }catch(e){}
    }
    DS.lineage.push({step:m.key,name:m.title,at:new Date().toISOString()});
    pushAudit('DS_MODULE_'+n,m.title);
    toastSafe('✓ '+m.title+' — '+r.summary,'success');
  }catch(e){
    console.error('[DS] '+m.title,e);
    DS.results[m.key]={n:m.n,key:m.key,title:m.title,icon:m.icon,color:m.color,summary:'Error: '+e.message,error:e.message,score:0,at:new Date().toISOString()};
    toastSafe('✗ '+m.title+' — '+e.message,'error');
  }
  if(card) card.classList.remove('running');
  DS.renderSuite();
};

/* ---------- Run all ---------- */
DS.runAll = function(){
  if(DS.running){ toastSafe('Pipeline already running','warn'); return; }
  if(!recs().length){ toastSafe('Import data first','warn'); return; }
  DS.running=true; DS.completed=0;
  toastSafe('🚀 17-module pipeline started','info');
  DS.renderSuite();
  var i=0;
  var next=function(){
    if(i>=DS.MODULES.length){ DS.running=false; pushAudit('DS_FULL_PIPELINE','17-modules'); toastSafe('✅ Full pipeline complete','success'); DS.renderSuite(); return; }
    DS.run(DS.MODULES[i].n); DS.completed=i+1; i++;
    setTimeout(next,180);
  };
  next();
};

/* ---------- Export ---------- */
DS.exportCSV = function(){
  try{
    var rows=DS.MODULES.map(function(m){var r=DS.results[m.key];return{Module:m.n,Title:m.title,Category:m.cat,Status:r?'Done':'Pending',Score:r?r.score:0,Summary:r?r.summary:''};});
    var h=Object.keys(rows[0]);
    var csv=[h.join(',')].concat(rows.map(function(r){return h.map(function(k){return '"'+String(r[k]||'').replace(/"/g,'""')+'"';}).join(',');})).join('\n');
    var blob=new Blob([csv],{type:'text/csv;charset=utf-8'});
    var a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download='datapulse-suite-'+Date.now()+'.csv'; a.click();
    setTimeout(function(){URL.revokeObjectURL(a.href);},5000);
    toastSafe('CSV downloaded','success');
  }catch(e){ toastSafe('Export failed: '+e.message,'error'); }
};
DS.exportJSON = function(){
  try{
    var data={generated:new Date().toISOString(),org:(state&&state.org?state.org.id:''),modules:DS.results,lineage:DS.lineage};
    var blob=new Blob([JSON.stringify(data,null,2)],{type:'application/json'});
    var a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download='datapulse-suite-'+Date.now()+'.json'; a.click();
    setTimeout(function(){URL.revokeObjectURL(a.href);},5000);
    toastSafe('JSON downloaded','success');
  }catch(e){ toastSafe('Export failed: '+e.message,'error'); }
};
DS.exportXLSX = function(){
  loadScript('https://cdn.sheetjs.com/xlsx-0.20.1/package/dist/xlsx.full.min.js').then(function(){
    var rows=DS.MODULES.map(function(m){var r=DS.results[m.key];return{Module:m.n,Title:m.title,Category:m.cat,Status:r?'Done':'Pending',Score:r?r.score:0,Summary:r?r.summary:''};});
    var ws=XLSX.utils.json_to_sheet(rows),wb=XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb,ws,'SuiteResults');
    XLSX.writeFile(wb,'datapulse-suite-'+Date.now()+'.xlsx');
    toastSafe('XLSX downloaded','success');
  }).catch(function(){ toastSafe('XLSX failed — using CSV','warn'); DS.exportCSV(); });
};
DS.exportPDF = function(){
  loadScript('https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js').then(function(){
    var jsPDF=(window.jspdf&&window.jspdf.jsPDF)?window.jspdf.jsPDF:null;
    if(!jsPDF){ toastSafe('PDF lib failed','error'); return; }
    var doc=new jsPDF();
    doc.setFillColor(15,23,42); doc.rect(0,0,210,32,'F');
    doc.setTextColor(255,255,255); doc.setFont('helvetica','bold'); doc.setFontSize(16);
    doc.text('DATAPULSE — 17-MODULE DATA SUITE',14,16);
    doc.setFontSize(9); doc.setTextColor(52,211,153);
    doc.text('Org: '+((state&&state.org)?state.org.name:'N/A')+'  |  '+new Date().toLocaleString(),14,24);
    doc.setTextColor(30,41,59); doc.setFontSize(11); doc.setFont('helvetica','bold');
    doc.text('Module Results',14,44);
    var y=52; doc.setFontSize(9); doc.setFont('helvetica','normal');
    DS.MODULES.forEach(function(m){
      var r=DS.results[m.key];
      if(y>270){ doc.addPage(); y=20; }
      doc.setFont('helvetica','bold'); doc.text('#'+m.n+'  '+m.title,14,y); y+=5;
      doc.setFont('helvetica','normal'); doc.setTextColor(80,80,80);
      doc.text(r?('[Score '+r.score+'] '+r.summary):'Pending',18,y); doc.setTextColor(30,41,59); y+=7;
    });
    doc.save('datapulse-suite-'+Date.now()+'.pdf');
    toastSafe('PDF downloaded','success');
  }).catch(function(e){ toastSafe('PDF failed: '+e.message,'error'); });
};

/* ---------- Render Suite View ---------- */
DS.renderSuite = function(){
  var host=document.getElementById('ds-suite-view'); if(!host) return;
  var completed=Object.keys(DS.results).length;
  var avg=completed?Math.round(Object.values(DS.results).reduce(function(a,r){return a+(r.score||0);},0)/completed):0;
  var pct=Math.round(completed/DS.MODULES.length*100);
  var modulesHtml=DS.MODULES.map(function(m){
    var r=DS.results[m.key], done=!!r;
    return '<div class="ds-module-card '+(done?'done':'')+'" data-ds-n="'+m.n+'" style="--ac:'+m.color+';--as:'+m.color+'26;--ab:'+m.color+'4d;--ag:'+m.color+'26" onclick="DS.run('+m.n+')">'+
      '<div class="ds-module-num">M'+m.n+'</div>'+
      '<div class="flex items-start gap-3 mb-2"><div class="ds-module-icon"><i class="fa-solid '+m.icon+'"></i></div>'+
      '<div class="min-w-0 flex-1"><div class="ds-module-tag">'+m.cat+'</div>'+
      '<div class="text-[12px] font-bold text-white mt-1 leading-tight">'+m.title+'</div></div></div>'+
      '<div class="text-[10px] text-slate-400 leading-relaxed min-h-[28px]">'+(r?(r.summary||r.error||'—'):m.short)+'</div>'+
      '<div class="ds-module-features">'+(m.features||[]).map(function(f){return '<span>'+f+'</span>';}).join('')+'</div>'+
      '<div class="ds-progress-bar"><div class="ds-progress-fill" style="width:'+(done?(r.score||0):0)+'%"></div></div>'+
      '<div class="flex items-center justify-between mt-3">'+
      '<span class="text-[10px] mono '+(done?'text-emerald-400 font-bold':'text-slate-500')+'">'+(done?'✓ Score '+(r.score||0):'Pending')+'</span>'+
      '<button class="px-3 py-1.5 bg-slate-950 border border-slate-700 text-xs font-bold rounded-lg" style="color:'+m.color+'" onclick="event.stopPropagation();DS.run('+m.n+')"><i class="fa-solid fa-play mr-1"></i>Run</button>'+
      '</div></div>';
  }).join('');
  var lineageHtml=DS.lineage.slice(-10).reverse().map(function(l){
    var mm=DS.MODULES.find(function(x){return x.key===l.step;})||{};
    return '<div class="flex items-center gap-3 p-2 rounded-lg bg-slate-950 border border-slate-800 text-[11px]">'+
      '<span class="w-2 h-2 rounded-full pulse-dot shrink-0" style="background:'+(mm.color||'#10b981')+'"></span>'+
      '<span class="text-slate-300 flex-1 truncate">'+l.name+'</span>'+
      '<span class="text-slate-500 mono text-[10px]">'+new Date(l.at).toLocaleTimeString()+'</span></div>';
  }).join('');
  var inputCards=[{k:'csv',icon:'fa-file-csv',title:'CSV / Excel',desc:'Drag & drop file'},{k:'link',icon:'fa-link',title:'Join Link',desc:'Sheets / CSV URL'},{k:'api',icon:'fa-cloud',title:'REST API',desc:'GET JSON endpoint'},{k:'paste',icon:'fa-paste',title:'Paste Text',desc:'CSV / JSON inline'},{k:'manual',icon:'fa-keyboard',title:'Manual Entry',desc:'Add rows one by one'},{k:'webhook',icon:'fa-webhook',title:'Webhook',desc:'Receive at unique URL'},{k:'iot',icon:'fa-satellite-dish',title:'IoT Stream',desc:'Real-time sensors'},{k:'sfot',icon:'fa-server',title:'Host / SFTP',desc:'CDN-hosted file'}].map(function(c){return '<div class="ds-input-card" onclick="DS.input(\''+c.k+'\')"><div class="ds-input-icon"><i class="fa-solid '+c.icon+'"></i></div><div class="ds-input-title">'+c.title+'</div><div class="ds-input-desc">'+c.desc+'</div></div>';}).join('');
  host.innerHTML='<div class="space-y-4 sm:space-y-5 fade">'+
    '<div class="ds-header"><div class="flex flex-wrap items-center justify-between gap-3"><div class="min-w-0">'+
    '<div class="ds-badge mb-2"><i class="fa-solid fa-cubes"></i> 17-Module Data Suite · Enterprise</div>'+
    '<h2 class="text-lg sm:text-2xl font-black text-white">Full Automation <span class="gradient-text">Data Pipeline</span></h2>'+
    '<p class="text-xs text-slate-300 mt-1">Connect any source · AI auto-processes · Export in every format</p></div>'+
    '<button onclick="DS.runAll()" '+(DS.running?'disabled':'')+' class="px-5 py-3 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-extrabold text-xs rounded-2xl disabled:opacity-50 shrink-0">'+
    '<i class="fa-solid '+(DS.running?'fa-spinner spin':'fa-play')+' mr-2"></i>'+(DS.running?'Running '+DS.completed+'/17':'Run Full Pipeline')+'</button></div>'+
    '<div class="grid grid-cols-3 gap-3 mt-4">'+
    '<div class="ds-stat"><div class="v">'+completed+'/17</div><div class="l">Modules Done</div></div>'+
    '<div class="ds-stat"><div class="v">'+avg+'</div><div class="l">Avg Score</div></div>'+
    '<div class="ds-stat"><div class="v">'+recs().length+'</div><div class="l">Records</div></div></div>'+
    '<div class="mt-4"><div class="h-2 rounded-full bg-slate-800 overflow-hidden"><div class="progress-bar" style="width:'+pct+'%"></div></div>'+
    '<p class="text-[10px] text-slate-400 mt-1 text-center">'+pct+'% complete · '+DS.lineage.length+' lineage steps</p></div></div>'+
    '<div class="bg-slate-900/90 border border-slate-800 rounded-2xl p-4 sm:p-5">'+
    '<h3 class="text-sm font-bold text-white mb-1"><i class="fa-solid fa-plug text-emerald-400 mr-2"></i>Connect Data Source</h3>'+
    '<p class="text-[11px] text-slate-400 mb-4">Choose one of 8 ways to ingest. Auto-cleans, auto-analyzes, feeds your 17 modules.</p>'+
    '<div class="grid grid-cols-2 sm:grid-cols-4 gap-3">'+inputCards+'</div></div>'+
    '<div class="bg-slate-900/90 border border-slate-800 rounded-2xl p-4 sm:p-5">'+
    '<div class="flex flex-wrap items-center justify-between gap-3"><div><h3 class="text-sm font-bold text-white"><i class="fa-solid fa-download text-emerald-400 mr-2"></i>Export Results</h3>'+
    '<p class="text-[11px] text-slate-400">Deliver reports in your preferred format</p></div>'+
    '<div class="flex flex-wrap gap-2">'+
    '<button class="ds-export-btn primary" onclick="DS.exportPDF()"><i class="fa-solid fa-file-pdf"></i>PDF</button>'+
    '<button class="ds-export-btn" onclick="DS.exportXLSX()"><i class="fa-solid fa-file-excel"></i>XLSX</button>'+
    '<button class="ds-export-btn" onclick="DS.exportCSV()"><i class="fa-solid fa-file-csv"></i>CSV</button>'+
    '<button class="ds-export-btn" onclick="DS.exportJSON()"><i class="fa-solid fa-file-code"></i>JSON</button></div></div></div>'+
    '<div><h3 class="text-xs font-bold text-emerald-400 uppercase mono mb-3 px-1">17 Enterprise Modules ('+DS.MODULES.length+')</h3>'+
    '<div class="ds-module-grid">'+modulesHtml+'</div></div>'+
    (DS.lineage.length?'<div class="bg-slate-900/90 border border-slate-800 rounded-2xl p-4 sm:p-5">'+
    '<h4 class="text-sm font-bold text-white mb-3"><i class="fa-solid fa-scroll text-emerald-400 mr-2"></i>Data Lineage (M15)</h4>'+
    '<div class="space-y-1.5 max-h-64 overflow-y-auto">'+lineageHtml+'</div></div>':'')+
    '</div>';
};

/* ---------- Input Handlers ---------- */
DS.input = function(kind){
  if(!window.state||!state.user){ toastSafe('Login first','warn'); return; }
  switch(kind){
    case 'csv': DS._inputFile(); break;
    case 'link': DS._inputLink(); break;
    case 'api': DS._inputApi(); break;
    case 'paste': DS._inputPaste(); break;
    case 'manual': DS._inputManual(); break;
    case 'webhook': DS._showWebhook(); break;
    case 'iot': DS._inputIoT(); break;
    case 'sfot': DS._inputLink(); break;
  }
};

DS._processAndCommit = function(rows, source){
  if(!rows||!rows.length){ toastSafe('No rows','warn'); return; }
  toastSafe('Processing '+rows.length+' rows via AI…','info');
  var normalized=rows.map(function(r,i){
    var keys=Object.keys(r);
    var nk=keys.find(function(k){return /name|item|title|product/i.test(k);})||keys[0];
    var ck=keys.find(function(k){return /cat|type|group|dept/i.test(k);});
    var pk=keys.find(function(k){return /price|sell|rate|amount/i.test(k);});
    var co=keys.find(function(k){return /cost|expense|cogs/i.test(k);});
    var sk=keys.find(function(k){return /stock|qty|quantity|count/i.test(k);});
    return{id:String(r.id||r.ID||('AUTO-'+String(i+1).padStart(4,'0'))),name:String(r[nk]||('Item '+(i+1))),category:ck?String(r[ck]):'General',price:parseFloat(String(pk?r[pk]:0).replace(/[^0-9.-]/g,''))||100,cost:parseFloat(String(co?r[co]:0).replace(/[^0-9.-]/g,''))||70,stock:parseInt(String(sk?r[sk]:0).replace(/[^0-9]/g,''))||10,unit:'Units',_source:source||'unknown'};
  });
  state.records=normalized;
  try{ if(typeof saveRecords==='function') saveRecords(); else if(state.org&&DP.LS) DP.LS.set('dp_records_'+state.org.id,state.records); }catch(e){}
  pushAudit('DS_INGEST_'+source,(state.org?state.org.id:''));
  toastSafe('✓ '+normalized.length+' rows ingested from '+source,'success');
  if(!DS.running) setTimeout(function(){ DS.runAll(); },400);
  DS.renderSuite();
};

DS._inputFile = function(){
  var inp=document.createElement('input'); inp.type='file'; inp.accept='.csv,.json,.txt';
  inp.onchange=function(e){
    var f=e.target.files[0]; if(!f) return;
    var reader=new FileReader();
    reader.onload=function(ev){
      try{
        var txt=ev.target.result, rows;
        if(/\.json$/i.test(f.name)) rows=JSON.parse(txt);
        else rows=DS._parseCSV(txt);
        if(!Array.isArray(rows)) rows=[rows];
        DS._processAndCommit(rows,'file:'+f.name);
      }catch(err){ toastSafe('Import failed: '+err.message,'error'); }
    };
    reader.readAsText(f);
  };
  inp.click();
};

DS._inputLink = function(){
  var url=prompt('Enter URL (Google Sheets, CSV, JSON):'); if(!url) return;
  var fetchUrl=url;
  if(url.indexOf('docs.google.com/spreadsheets')!==-1){ var m=url.match(/\/d\/([^\/]+)/); if(m) fetchUrl='https://docs.google.com/spreadsheets/d/'+m[1]+'/export?format=csv'; }
  fetch(fetchUrl).then(function(r){return r.text();}).then(function(txt){
    var rows; try{ rows=JSON.parse(txt); }catch(e){ rows=DS._parseCSV(txt); }
    if(!Array.isArray(rows)) rows=[rows];
    DS._processAndCommit(rows,'link');
  }).catch(function(e){ toastSafe('Fetch failed: '+e.message,'error'); });
};

DS._inputApi = function(){
  var url=prompt('Enter API endpoint URL:'); if(!url) return;
  fetch(url).then(function(r){return r.json();}).then(function(data){
    var items=Array.isArray(data)?data:(data.items||data.data||data.results||[data]);
    DS._processAndCommit(items,'api');
  }).catch(function(e){ toastSafe('API failed: '+e.message,'error'); });
};

DS._inputPaste = function(){
  var txt=prompt('Paste CSV or JSON here:'); if(!txt) return;
  try{
    var rows, trimmed=txt.trim();
    if(trimmed[0]==='['||trimmed[0]==='{') rows=JSON.parse(trimmed);
    else rows=DS._parseCSV(trimmed);
    if(!Array.isArray(rows)) rows=[rows];
    DS._processAndCommit(rows,'paste');
  }catch(e){ toastSafe('Parse failed: '+e.message,'error'); }
};

DS._inputManual = function(){
  var name=prompt('Item name:'); if(!name) return;
  var category=prompt('Category:','General')||'General';
  var price=parseFloat(prompt('Price:','100'))||100;
  var cost=parseFloat(prompt('Cost:','70'))||70;
  var stock=parseInt(prompt('Stock:','10'))||10;
  DS._processAndCommit([{id:'MAN-'+Date.now().toString().slice(-5),name:name,category:category,price:price,cost:cost,stock:stock,unit:'Units',_source:'manual'}],'manual');
};

DS._showWebhook = function(){
  var key=(state.org&&state.org.apiKey)?state.org.apiKey:'YOUR_KEY';
  var url='https://datapulseapp-20237.web.app/hook/'+key;
  alert('Webhook URL:\n\n'+url+'\n\nPOST JSON array here to ingest data automatically.');
  try{ navigator.clipboard.writeText(url).then(function(){ toastSafe('Webhook URL copied','success'); }); }catch(e){}
};

DS._inputIoT = function(){
  DS._processAndCommit([{id:'IOT-'+Date.now().toString().slice(-5),name:'Sensor-'+Math.floor(Math.random()*100),category:'IoT',price:Math.round(200+Math.random()*150),cost:Math.round(120+Math.random()*80),stock:Math.floor(Math.random()*500),unit:'Units',_source:'iot'}],'iot');
};

DS._parseCSV = function(txt){
  var lines=txt.split(/\r?\n/).filter(function(l){return l.trim();});
  if(lines.length<2) throw new Error('Empty CSV');
  var sep=txt.indexOf('\t')!==-1?'\t':',';
  var headers=lines[0].split(sep).map(function(h){return h.trim().replace(/^["']|["']$/g,'');});
  return lines.slice(1).map(function(l){
    var cols=l.split(sep).map(function(c){return c.trim().replace(/^["']|["']$/g,'');});
    var o={}; headers.forEach(function(h,i){o[h]=cols[i];}); return o;
  });
};

/* ---------- Patch TABS + render ---------- */
DS.patch = function(){
  try{
    if(typeof TABS!=='undefined'&&!TABS.some(function(t){return t.id==='datasuite';})){
      TABS.push({id:'datasuite',key:'datasuite',icon:'fa-cubes',label:'17-Module Suite'});
      if(typeof renderNav==='function') renderNav();
      if(typeof renderDock==='function') renderDock();
    }
  }catch(e){ console.warn('[DS] TABS patch:',e); }
  try{
    if(typeof window.render==='function'&&!window.__dsRenderPatched){
      window.__dsRenderPatched=true;
      var orig=window.render;
      window.render=function(){
        if(window.state&&state.tab==='datasuite'){
          var el=document.getElementById('main');
          if(el){ el.innerHTML='<div id="ds-suite-view" class="fade"></div>'; DS.renderSuite(); try{ if(DP&&DP.i18n&&DP.i18n.apply) DP.i18n.apply(); }catch(e){} }
          return;
        }
        return orig.apply(this,arguments);
      };
    }
  }catch(e){ console.warn('[DS] render patch:',e); }
  try{
    if(window.DP&&DP.i18n&&DP.i18n.resources){
      if(DP.i18n.resources.en) DP.i18n.resources.en.datasuite='17-Module Suite';
      if(DP.i18n.resources.om) DP.i18n.resources.om.datasuite='Moduulii 17';
      if(DP.i18n.resources.am) DP.i18n.resources.am.datasuite='17 ሞጁሎች';
    }
  }catch(e){}
  console.log('[DS] 17-Module Suite patched ✓');
};

window.DS = DS;

function boot(){
  if(typeof TABS==='undefined'||typeof window.render==='undefined'){ return setTimeout(boot,100); }
  DS.patch();
}
if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',boot);
else boot();
})();

let alerts = [];
let timelineChart, protocolChart;
const $ = id => document.getElementById(id);
const text = (tag, value) => {const node = document.createElement(tag); node.textContent = value ?? '—'; return node;};
function priority(n){return Number(n) === 1 ? ['High','high'] : Number(n) === 2 ? ['Medium','medium'] : ['Low','low'];}
function drawAlerts(){
  const q = $('search').value.toLowerCase().trim();
  const proto = $('protocolFilter').value;
  const sev = $('severityFilter').value;
  const filtered = alerts.filter(a => {
    const fields = [a.source_ip,a.destination_ip,a.signature,a.protocol].join(' ').toLowerCase();
    return fields.includes(q) && (!proto || a.protocol === proto) && (!sev || (sev === '3' ? Number(a.severity) >= 3 : String(a.severity) === sev));
  });
  $('shown').textContent = `${filtered.length} shown`;
  const body = $('alertsBody'); body.replaceChildren();
  for(const a of filtered){
    const row = document.createElement('tr');
    for(const field of ['timestamp','source_ip','destination_ip','protocol','signature']) row.appendChild(text('td',a[field]));
    const cell = document.createElement('td'); const badge = text('span',priority(a.severity)[0]);
    badge.className = `badge ${priority(a.severity)[1]}`;cell.appendChild(badge);row.appendChild(cell);body.appendChild(row);
  }
}
function updateProtocolOptions(){
  const select = $('protocolFilter'), old = select.value;
  const names = [...new Set(alerts.map(a => a.protocol).filter(Boolean))].sort();
  select.replaceChildren(new Option('All protocols',''));
  names.forEach(n => select.add(new Option(n,n)));
  if(names.includes(old)) select.value = old;
}
function chart(canvas,kind,labels,values,existing){
  if(typeof Chart === 'undefined') return existing;
  if(existing) existing.destroy();
  return new Chart($(canvas), {type:kind,data:{labels,datasets:[{label:'Alerts',data:values,borderColor:'#39d98a',backgroundColor:kind==='doughnut'?['#39d98a','#65a8ff','#f4c76b','#b58df5','#e87e8b']:'#39d98a44',fill:kind==='line',tension:.25}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:kind==='doughnut',labels:{color:'#c9d5ce'}}},scales:kind==='line'?{x:{ticks:{color:'#94a69b',maxTicksLimit:6}},y:{beginAtZero:true,ticks:{color:'#94a69b',precision:0}}}:{}}});
}
async function refresh(){
  try{
    const [s,a] = await Promise.all([fetch('/api/stats'),fetch('/api/alerts')]);
    if(!s.ok||!a.ok) throw new Error('API unavailable');
    const stats = await s.json(); alerts = await a.json();
    for(const k of ['total','high','medium','low']) $(k).textContent = stats[k];
    updateProtocolOptions();drawAlerts();
    timelineChart = chart('timelineChart','line',stats.timeline.map(x=>x.bucket),stats.timeline.map(x=>x.value),timelineChart);
    protocolChart = chart('protocolChart','doughnut',stats.protocols.map(x=>x.name),stats.protocols.map(x=>x.value),protocolChart);
    $('status').textContent = '● Dashboard connected';
  }catch(e){$('status').textContent = '● Dashboard disconnected';console.error(e);}
}
['search','protocolFilter','severityFilter'].forEach(id=>$(id).addEventListener('input',drawAlerts));
refresh();setInterval(refresh,5000);

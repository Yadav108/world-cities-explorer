content = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>🌐 Urban Analytics</title>
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    :root {
      --bg: #0d0d1a; --bg2: #12122a; --border: #1e1e3a; --border2: #2a2a4a;
      --accent: #00cfff; --accent-b: #ff9f43; --text: #cdd6f4; --text2: #7799bb;
      --panel-w: 300px; --header-h: 60px;
    }
    body { font-family: 'Segoe UI', Arial, sans-serif; background: var(--bg); color: var(--text); height: 100vh; overflow: hidden; }

    /* Header */
    #header {
      position: fixed; top: 0; left: 0; right: 0; height: var(--header-h);
      background: var(--bg2); border-bottom: 1px solid var(--border);
      display: flex; align-items: center; padding: 0 20px; gap: 12px; z-index: 2000;
    }
    #hdr-title { font-size: 1rem; font-weight: 700; white-space: nowrap; }
    #hdr-country { color: var(--accent); font-weight: 700; font-size: 0.9rem; }
    #hdr-status { font-size: 0.75rem; color: var(--text2); }
    .toggle-wrap { margin-left: auto; display: flex; gap: 8px; }
    .toggle-btn {
      background: #1a1a2e; color: #7799bb; border: 1px solid #2a2a4a;
      border-radius: 20px; padding: 6px 16px; font-size: 0.8rem; cursor: pointer;
      transition: all 0.2s;
    }
    .toggle-btn.active { background: var(--accent); color: #0d0d1a; font-weight: 700; border-color: var(--accent); }
    .toggle-btn:not(.active):hover { border-color: var(--accent); color: var(--accent); }

    /* Map */
    #map { position: fixed; top: var(--header-h); left: 0; right: var(--panel-w); bottom: 0; }

    /* Panel */
    #panel {
      position: fixed; top: var(--header-h); right: 0; width: var(--panel-w); bottom: 0;
      background: var(--bg2); border-left: 1px solid var(--border);
      overflow-y: auto; z-index: 1000; padding: 16px;
    }
    #panel::-webkit-scrollbar { width: 5px; }
    #panel::-webkit-scrollbar-track { background: var(--bg); }
    #panel::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 3px; }

    /* Panel section title */
    .p-title {
      font-size: 0.68rem; letter-spacing: 0.1em; color: var(--text2);
      text-transform: uppercase; margin-bottom: 14px; padding-bottom: 6px;
      border-bottom: 1px solid var(--border);
    }

    /* Gravity panel */
    .pair-row {
      display: flex; flex-direction: column; gap: 4px;
      padding: 10px 0; border-bottom: 1px solid var(--border);
    }
    .pair-row:last-child { border-bottom: none; }
    .pair-top { display: flex; align-items: center; gap: 8px; font-size: 0.78rem; }
    .pair-rank { color: var(--text2); width: 18px; flex-shrink: 0; }
    .pair-name { flex: 1; color: var(--text); }
    .pair-score { color: var(--accent-b); font-weight: 700; font-size: 0.75rem; }
    .pair-bar-bg { height: 4px; background: var(--border2); border-radius: 2px; margin-top: 2px; }
    .pair-bar-fg { height: 4px; background: var(--accent-b); border-radius: 2px; }
    .pair-dist { font-size: 0.68rem; color: var(--text2); }

    /* Concentration panel */
    .conf-badge {
      display: inline-block; font-size: 0.72rem; font-weight: 700;
      padding: 3px 10px; border-radius: 12px; margin-bottom: 10px; letter-spacing: 0.04em;
    }
    .conf-note { font-size: 0.7rem; color: var(--accent-b); margin-bottom: 14px; line-height: 1.5; }
    .stat-row {
      display: flex; justify-content: space-between; font-size: 0.78rem;
      padding: 6px 0; border-bottom: 1px solid var(--border);
    }
    .stat-row:last-child { border-bottom: none; }
    .stat-label { color: var(--text2); }
    .stat-val   { color: var(--text); font-weight: 600; }
    .section-gap { margin-top: 20px; }

    /* Tooltip */
    #tooltip {
      position: fixed; background: rgba(13,13,26,0.93); border: 1px solid #1e1e3a;
      border-radius: 8px; padding: 10px 14px; pointer-events: none; font-size: 0.82rem;
      color: #cdd6f4; display: none; z-index: 9000; max-width: 220px;
      line-height: 1.6; backdrop-filter: blur(6px);
    }
    #tooltip .tt-title { font-weight: 700; color: var(--accent); margin-bottom: 3px; }
    #tooltip .tt-title.pair { color: var(--accent-b); }
    #tooltip .tt-sub { color: var(--text2); font-size: 0.76rem; }
    #tooltip .tt-val { color: var(--text); font-weight: 600; }

    /* Loading / error */
    #status-overlay {
      position: fixed; top: var(--header-h); left: 0; right: var(--panel-w); bottom: 0;
      background: rgba(13,13,26,0.85); display: flex; flex-direction: column;
      align-items: center; justify-content: center; z-index: 1500; gap: 12px;
    }
    #status-overlay.hidden { display: none; }
    .spinner { width: 36px; height: 36px; border: 3px solid var(--border2); border-top-color: var(--accent); border-radius: 50%; animation: spin 0.7s linear infinite; }
    @keyframes spin { to { transform: rotate(360deg); } }
    #status-msg { color: var(--text2); font-size: 0.85rem; }

    /* Pulse animation */
    @keyframes pulse { 0% { stroke-dashoffset: 200; } 100% { stroke-dashoffset: 0; } }
  </style>
</head>
<body>

<header id="header">
  <span id="hdr-title">🌐 Urban Analytics</span>
  <span id="hdr-country"></span>
  <span id="hdr-status" style="color:var(--text2);font-size:0.75rem;">Loading data…</span>
  <div class="toggle-wrap">
    <button class="toggle-btn active" id="btn-gravity"        onclick="switchMode('gravity')">⚡ Gravity</button>
    <button class="toggle-btn"        id="btn-concentration"  onclick="switchMode('concentration')">📊 Concentration</button>
  </div>
</header>

<div id="map"></div>
<div id="panel"></div>
<div id="tooltip"></div>

<div id="status-overlay">
  <div class="spinner"></div>
  <div id="status-msg">Loading gravity_data.json &amp; concentration.json…</div>
</div>

<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script src="https://d3js.org/d3.v7.min.js"></script>
<script>
// ════════════════════════════════════════════════
//  STATE
// ════════════════════════════════════════════════
let currentMode       = 'gravity';
let gravityData       = null;
let concentrationData = null;

// ════════════════════════════════════════════════
//  MAP SETUP
// ════════════════════════════════════════════════
const map = L.map('map', { zoomControl: true }).setView([51.2, 10.4], 6);
L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
  attribution: '© OpenStreetMap © CARTO', maxZoom: 18
}).addTo(map);

L.svg().addTo(map);
const svg = d3.select('#map').select('svg').style('overflow', 'visible');
const g   = svg.append('g').attr('class', 'leaflet-zoom-hide');

const project = (lng, lat) => map.latLngToLayerPoint(new L.LatLng(lat, lng));

// ════════════════════════════════════════════════
//  REPROJECT  (handles both modes)
// ════════════════════════════════════════════════
function reproject() {
  g.selectAll('line.gravity-line, line.pulse-line')
    .attr('x1', d => project(d.lng_a, d.lat_a).x)
    .attr('y1', d => project(d.lng_a, d.lat_a).y)
    .attr('x2', d => project(d.lng_b, d.lat_b).x)
    .attr('y2', d => project(d.lng_b, d.lat_b).y);
  g.selectAll('circle.city-node')
    .attr('cx', d => project(d.lng, d.lat).x)
    .attr('cy', d => project(d.lng, d.lat).y);
}
map.on('zoomend moveend viewreset', reproject);

// ════════════════════════════════════════════════
//  TOOLTIP
// ════════════════════════════════════════════════
const tip    = document.getElementById('tooltip');
const fmtPop = d3.format(',');
const fmtPct = v => v.toFixed(1) + '%';

function showTip(html, ev) { tip.innerHTML = html; tip.style.display = 'block'; moveTip(ev); }
function moveTip(ev) {
  tip.style.left = Math.min(ev.clientX + 14, window.innerWidth  - 230) + 'px';
  tip.style.top  = Math.min(ev.clientY - 10, window.innerHeight - 130) + 'px';
}
function hideTip() { tip.style.display = 'none'; }

// ════════════════════════════════════════════════
//  COLOUR HELPERS
// ════════════════════════════════════════════════
function primacyColor(p)    { return p < 0.15 ? '#00cfff' : p < 0.35 ? '#ff9f43' : '#ff4757'; }
function primacyCategory(p) { return p < 0.15 ? 'Distributed' : p < 0.35 ? 'Moderate' : 'Dominant'; }
const RANK_COLORS = ['#ff4757','#ff9f43','#ffd32a','#7bed9f','#70a1ff'];

// ════════════════════════════════════════════════
//  GRAVITY MAP
// ════════════════════════════════════════════════
function drawGravityMap() {
  const cities = gravityData.cities;
  const pairs  = gravityData.pairs;

  const [minP, maxP] = d3.extent(cities, d => d.population);
  const [minG, maxG] = d3.extent(pairs,  d => d.gravity);
  const radScale   = d3.scaleSqrt().domain([minP, maxP]).range([4, 20]);
  const wScale     = d3.scaleLinear().domain([minG, maxG]).range([1, 6]);
  const opacScale  = d3.scaleLinear().domain([minG, maxG]).range([0.2, 0.9]);

  // Base lines
  g.selectAll('line.gravity-line')
    .data(pairs).join('line').attr('class', 'gravity-line')
    .attr('stroke', '#ff9f43')
    .attr('stroke-width',   d => wScale(d.gravity))
    .attr('stroke-opacity', d => opacScale(d.gravity))
    .attr('stroke-linecap', 'round').attr('cursor', 'pointer')
    .on('mouseover', (ev, d) => showTip(`
      <div class="tt-title pair">${d.city_a} → ${d.city_b}</div>
      <div class="tt-sub">Gravity: <span class="tt-val">${d.gravity.toFixed(4)}</span></div>
      <div class="tt-sub">Distance: <span class="tt-val">${d.distance_km} km</span></div>
      <div class="tt-sub">${d.city_a}: <span class="tt-val">${fmtPop(d.pop_a)}</span></div>
      <div class="tt-sub">${d.city_b}: <span class="tt-val">${fmtPop(d.pop_b)}</span></div>
    `, ev))
    .on('mousemove', moveTip).on('mouseout', hideTip);

  // Pulse lines
  g.selectAll('line.pulse-line')
    .data(pairs).join('line').attr('class', 'pulse-line')
    .attr('stroke', '#ffffff')
    .attr('stroke-width',     d => 1 + d.gravity * 3)
    .attr('stroke-dasharray', '8 192')
    .attr('stroke-linecap',   'round')
    .attr('opacity',          d => 0.4 + d.gravity * 0.6)
    .attr('pointer-events',   'none')
    .style('animation', d => `pulse ${(3 - d.gravity * 2).toFixed(2)}s linear infinite`);

  // City circles
  g.selectAll('circle.city-node')
    .data(cities).join('circle').attr('class', 'city-node')
    .attr('r',            d => radScale(d.population))
    .attr('fill',         '#00cfff')
    .attr('fill-opacity', 0.85)
    .attr('stroke',       '#0d0d1a').attr('stroke-width', 1.5)
    .attr('cursor',       'pointer')
    .on('mouseover', (ev, d) => showTip(`
      <div class="tt-title">#${d.rank} ${d.city}</div>
      <div class="tt-sub">Population: <span class="tt-val">${fmtPop(d.population)}</span></div>
    `, ev))
    .on('mousemove', moveTip).on('mouseout', hideTip);

  reproject();
  const lats = cities.map(c => c.lat), lngs = cities.map(c => c.lng);
  map.fitBounds([[d3.min(lats), d3.min(lngs)], [d3.max(lats), d3.max(lngs)]], { padding: [50, 50] });
}

// ════════════════════════════════════════════════
//  CONCENTRATION MAP  (circles from gravity coords)
// ════════════════════════════════════════════════
function drawConcentrationMap() {
  // Look up lat/lng from gravityData.cities by name
  const coordMap = {};
  gravityData.cities.forEach(c => { coordMap[c.city] = c; });

  const top5 = concentrationData.top5
    .map(d => ({ ...d, ...(coordMap[d.city] || {}) }))
    .filter(d => d.lat != null);

  const [minS, maxS] = d3.extent(top5, d => d.share_pct);
  const radScale = d3.scaleSqrt().domain([minS, maxS]).range([6, 28]);

  g.selectAll('circle.city-node')
    .data(top5).join('circle').attr('class', 'city-node')
    .attr('r',            d => radScale(d.share_pct))
    .attr('fill',         (_, i) => RANK_COLORS[i] || '#cdd6f4')
    .attr('fill-opacity', 0.88)
    .attr('stroke',       '#0d0d1a').attr('stroke-width', 1.5)
    .attr('cursor',       'pointer')
    .on('mouseover', (ev, d) => showTip(`
      <div class="tt-title" style="color:${RANK_COLORS[d.rank-1]}">#${d.rank} ${d.city}</div>
      <div class="tt-sub">Share: <span class="tt-val">${fmtPct(d.share_pct)}</span></div>
      <div class="tt-sub">Population: <span class="tt-val">${fmtPop(d.population)}</span></div>
    `, ev))
    .on('mousemove', moveTip).on('mouseout', hideTip);

  reproject();
}

// ════════════════════════════════════════════════
//  GRAVITY PANEL
// ════════════════════════════════════════════════
function drawGravityPanel() {
  const p     = d3.select('#panel');
  const pairs = gravityData.pairs;

  p.append('div').attr('class', 'p-title').text('Gravity Pairs');

  // Summary line
  const strongest = pairs[0];
  p.append('div').style('font-size','0.72rem').style('color','var(--text2)')
   .style('margin-bottom','14px')
   .html(`${pairs.length} pairs &nbsp;·&nbsp; Strongest: <span style="color:var(--accent-b);font-weight:700">${strongest.city_a} → ${strongest.city_b}</span>`);

  pairs.forEach((d, i) => {
    const row = p.append('div').attr('class', 'pair-row');
    const top = row.append('div').attr('class', 'pair-top');
    top.append('span').attr('class', 'pair-rank').text(`${i+1}`);
    top.append('span').attr('class', 'pair-name').text(`${d.city_a} → ${d.city_b}`);
    top.append('span').attr('class', 'pair-score').text(d.gravity.toFixed(3));
    const bg = row.append('div').attr('class', 'pair-bar-bg');
    bg.append('div').attr('class', 'pair-bar-fg').style('width', (d.gravity * 140) + 'px');
    row.append('div').attr('class', 'pair-dist').text(`${d.distance_km} km  ·  ${fmtPop(d.pop_a)} / ${fmtPop(d.pop_b)}`);
  });
}

// ════════════════════════════════════════════════
//  CONCENTRATION PANEL  (arc gauge + bar chart)
// ════════════════════════════════════════════════
function drawConcentrationPanel() {
  const p    = d3.select('#panel');
  const data = concentrationData;
  const color = primacyColor(data.primacy_index);

  p.append('div').attr('class', 'p-title').text('Primacy Index');

  // Confidence badge
  const badgeMeta = {
    high:   { bg:'rgba(46,213,115,0.15)', c:'#2ed573', t:'★★★ High Confidence'   },
    medium: { bg:'rgba(255,159,67,0.15)', c:'#ff9f43', t:'★★☆ Medium Confidence' },
    low:    { bg:'rgba(255,71,87,0.15)',  c:'#ff4757', t:'★☆☆ Low Confidence'    },
  }[data.confidence];
  p.append('div').attr('class','conf-badge')
   .style('background', badgeMeta.bg).style('color', badgeMeta.c)
   .style('border', `1px solid ${badgeMeta.c}44`)
   .text(badgeMeta.t);
  if (data.confidence_note)
    p.append('div').attr('class','conf-note').text('⚠️ ' + data.confidence_note);

  // Arc gauge SVG
  const gaugeSvg = p.append('svg')
    .attr('width', '100%').attr('viewBox','0 0 260 145')
    .style('overflow','visible').style('display','block');

  const arc = d3.arc().innerRadius(70).outerRadius(100).startAngle(-Math.PI/2);
  const cx = 130, cy = 118;
  const ag = gaugeSvg.append('g').attr('transform', `translate(${cx},${cy})`);

  // Track
  ag.append('path').datum({ endAngle: Math.PI/2 }).attr('d', arc).attr('fill','#1e1e3a');

  // Tick marks
  [0,0.25,0.5,0.75,1].forEach(v => {
    const a = -Math.PI/2 + v*Math.PI;
    ag.append('line')
      .attr('x1',Math.cos(a)*102).attr('y1',Math.sin(a)*102)
      .attr('x2',Math.cos(a)*112).attr('y2',Math.sin(a)*112)
      .attr('stroke','#2a2a4a').attr('stroke-width',1.5);
  });

  // Foreground arc — animated
  const endAngle = -Math.PI/2 + data.primacy_index * Math.PI;
  ag.append('path').datum({ endAngle: -Math.PI/2 })
    .attr('d', arc).attr('fill', color)
    .transition().duration(900).ease(d3.easeCubicOut)
    .attrTween('d', function(d) {
      const interp = d3.interpolate(d.endAngle, endAngle);
      return t => { d.endAngle = interp(t); return arc(d); };
    });

  // Labels
  ag.append('text').attr('text-anchor','middle').attr('dy','-0.2em')
    .attr('fill','#cdd6f4').attr('font-size','1.8rem').attr('font-weight',800)
    .text(fmtPct(data.primacy_index * 100));
  ag.append('text').attr('text-anchor','middle').attr('dy','1.2em')
    .attr('fill','#7799bb').attr('font-size','0.72rem')
    .text('in ' + data.largest_city.city);
  ag.append('text').attr('text-anchor','middle').attr('dy','2.6em')
    .attr('fill', color).attr('font-size','0.78rem').attr('font-weight',700)
    .attr('letter-spacing','0.07em')
    .text(primacyCategory(data.primacy_index).toUpperCase());
  ag.append('text').attr('x',-112).attr('y',14)
    .attr('fill','#555577').attr('font-size','0.6rem').text('0%');
  ag.append('text').attr('x',98).attr('y',14)
    .attr('fill','#555577').attr('font-size','0.6rem').text('100%');

  // ── Stat rows
  p.append('div').attr('class','section-gap');
  [
    ['Total cities',    data.total_cities],
    ['Total urban pop', fmtPop(data.total_population)],
    ['Top 5 share',     fmtPct(data.top5_combined_share)],
  ].forEach(([label, val]) => {
    const row = p.append('div').attr('class','stat-row');
    row.append('span').attr('class','stat-label').text(label);
    row.append('span').attr('class','stat-val').text(val);
  });

  // ── Top 5 bar chart
  p.append('div').attr('class','p-title section-gap').text('Top 5 Cities by Share');

  const barW = 230, rowH = 44, padLeft = 0;
  const labelW = 80, pctW = 44;
  const innerW = labelW + barW - pctW;

  const barSvg = p.append('svg')
    .attr('width','100%')
    .attr('viewBox', `0 0 ${barW} ${data.top5.length * rowH}`)
    .style('overflow','visible');

  const xScale = d3.scaleLinear()
    .domain([0, data.top5[0].share_pct])
    .range([0, barW - labelW - pctW]);

  data.top5.forEach((d, i) => {
    const gy = barSvg.append('g').attr('transform', `translate(0,${i*rowH + 4})`);
    const c  = RANK_COLORS[i];

    gy.append('text').attr('x',0).attr('y',14)
      .attr('fill','#555577').attr('font-size','0.65rem').text(`#${i+1}`);
    gy.append('text').attr('x',20).attr('y',14)
      .attr('fill','#cdd6f4').attr('font-size','0.75rem')
      .text(d.city.length > 11 ? d.city.slice(0,10)+'…' : d.city);

    gy.append('rect').attr('x',labelW).attr('y',2)
      .attr('width', barW-labelW-pctW).attr('height',18)
      .attr('rx',3).attr('fill','#1e1e3a');

    gy.append('rect').attr('x',labelW).attr('y',2)
      .attr('width',0).attr('height',18)
      .attr('rx',3).attr('fill',c).attr('opacity',0.85)
      .transition().duration(700).delay(i*80).ease(d3.easeCubicOut)
      .attr('width', xScale(d.share_pct));

    gy.append('text').attr('x', labelW + xScale(d.share_pct) + 5).attr('y',14)
      .attr('fill','#7799bb').attr('font-size','0.68rem')
      .text(fmtPct(d.share_pct));

    gy.append('text').attr('x',labelW).attr('y',32)
      .attr('fill','#555577').attr('font-size','0.62rem')
      .text(fmtPop(d.population));
  });
}

// ════════════════════════════════════════════════
//  RENDER ORCHESTRATION
// ════════════════════════════════════════════════
function renderMap() {
  g.selectAll('*').remove();
  if (currentMode === 'gravity') drawGravityMap();
  else drawConcentrationMap();
}

function renderPanel() {
  d3.select('#panel').html('');
  if (currentMode === 'gravity') drawGravityPanel();
  else drawConcentrationPanel();
}

function switchMode(mode) {
  currentMode = mode;
  document.getElementById('btn-gravity').classList.toggle('active', mode === 'gravity');
  document.getElementById('btn-concentration').classList.toggle('active', mode === 'concentration');
  if (gravityData && concentrationData) { renderMap(); renderPanel(); }
}

// ════════════════════════════════════════════════
//  DATA LOAD  (parallel, once)
// ════════════════════════════════════════════════
const overlay   = document.getElementById('status-overlay');
const statusMsg = document.getElementById('status-msg');

Promise.all([
  d3.json('gravity_data.json'),
  d3.json('concentration.json')
]).then(([gd, cd]) => {
  gravityData       = gd;
  concentrationData = cd;
  document.getElementById('hdr-country').textContent = gd.country;
  document.getElementById('hdr-status').textContent  = `${gd.meta.total_cities} cities · ${gd.meta.total_pairs} pairs`;
  overlay.classList.add('hidden');
  switchMode('gravity');
}).catch(() => {
  statusMsg.textContent = '⚠️ Data files not found — run: python generate_gravity.py';
  statusMsg.style.color = '#ff4757';
  document.querySelector('.spinner').style.display = 'none';
});
</script>
</body>
</html>"""

with open(r'C:\Users\Aryan\PycharmProjects\pythonProject\100 day challenge\index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Written successfully, size:", len(content))

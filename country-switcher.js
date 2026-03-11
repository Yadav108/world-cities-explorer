// country-switcher.js — Country Switcher Panel (Prompt 19)
// Self-contained. Requires d3 (for d3.json) and IS_LOCAL to be defined before loading.
// Place at root level, load AFTER d3.v7.min.js.

const CountrySwitcher = {

  allCountries:  [],   // from global_ranking.json
  pregenerated:  [
    'Germany','France','Japan','India','China',
    'United States','Brazil','Thailand','Australia',
    'United Kingdom','Italy','Spain','Canada','Mexico',
    'South Korea','Indonesia','Pakistan','Nigeria',
    'Egypt','Argentina','Russia','Turkey','Iran',
    'Vietnam','Philippines','Ethiopia','Tanzania',
    'Kenya','Colombia','Poland',
  ],
  currentCountry: null,
  onSwitch: null,

  // ── Init ──────────────────────────────────────────────────────
  async init(onSwitchCallback) {
    this.onSwitch = onSwitchCallback;

    try {
      const ranking = await d3.json('global_ranking.json');
      this.allCountries = ranking.map(d => ({
        name:    d.country,
        primacy: d.primacy_index,
        pattern: d.pattern || 'transitional',
        rank:    d.rank,
      }));
    } catch (e) {
      // global_ranking.json not yet generated — fall back to pregenerated list only
      this.allCountries = this.pregenerated.map((n, i) => ({
        name: n, primacy: 0, pattern: 'transitional', rank: i + 1,
      }));
    }

    this._render();
    this._injectTriggerButton();
  },

  // ── Open / Close ──────────────────────────────────────────────
  open() {
    document.getElementById('cs-overlay').classList.add('open');
    document.getElementById('cs-panel').classList.add('open');
    const inp = document.getElementById('cs-search');
    if (inp) { inp.value = ''; this.search(''); setTimeout(() => inp.focus(), 60); }
  },

  close() {
    document.getElementById('cs-overlay').classList.remove('open');
    document.getElementById('cs-panel').classList.remove('open');
  },

  // ── Search ────────────────────────────────────────────────────
  search(query) {
    const q = query.toLowerCase().trim();
    const preList = this.allCountries.filter(c =>
      this.pregenerated.some(p => p.toLowerCase() === c.name.toLowerCase()) &&
      c.name.toLowerCase().includes(q)
    );
    const pipeList = this.allCountries.filter(c =>
      !this.pregenerated.some(p => p.toLowerCase() === c.name.toLowerCase()) &&
      c.name.toLowerCase().includes(q)
    );

    document.getElementById('cs-pregenerated-list').innerHTML =
      this._buildListHTML(preList, true);

    const pipelineSection = document.getElementById('cs-pipeline-section');
    if (pipelineSection) {
      document.getElementById('cs-pipeline-list').innerHTML =
        this._buildListHTML(pipeList, false);
    }
  },

  // ── Select a country ─────────────────────────────────────────
  async selectCountry(name) {
    this.close();
    this.currentCountry = name;
    this._updateTrigger(name);

    // Show loading state via overlay
    const overlay  = document.getElementById('status-overlay');
    const statusEl = document.getElementById('status-msg');
    if (overlay && statusEl) {
      overlay.classList.remove('hidden');
      document.querySelector('.spinner').style.display = '';
    }

    const isPregenerated = this.pregenerated
      .some(c => c.toLowerCase() === name.toLowerCase());

    try {
      let gravity, concentration;

      if (isPregenerated || !IS_LOCAL) {
        // ⚡ Instant — load from data/ folder
        if (statusEl) statusEl.textContent = `Loading ${name}…`;
        const folder = `data/${name.replace(/ /g, '_')}`;
        [gravity, concentration] = await Promise.all([
          d3.json(`${folder}/gravity_data.json`),
          d3.json(`${folder}/concentration.json`),
        ]);
      } else {
        // 🔄 Run pipeline (local only)
        if (statusEl) statusEl.textContent = `Running pipeline for ${name}…`;
        const res = await fetch(`/run-pipeline?country=${encodeURIComponent(name)}`);
        if (!res.ok) {
          const err = await res.json().catch(() => ({}));
          throw new Error(err.error || `Server returned ${res.status}. Is server.py running?`);
        }
        const ts = Date.now();
        [gravity, concentration] = await Promise.all([
          d3.json(`gravity_data.json?t=${ts}`),
          d3.json(`concentration.json?t=${ts}`),
        ]);
      }

      if (this.onSwitch) {
        this.onSwitch({ gravity, concentration, country: name });
      }

    } catch (e) {
      if (statusEl) {
        statusEl.textContent = `❌ ${e.message}`;
        statusEl.style.color = '#ff4757';
      }
      if (overlay) document.querySelector('.spinner').style.display = 'none';
    }

    // Refresh active highlight
    this.search(document.getElementById('cs-search')?.value || '');
  },

  // ── Build list item HTML ──────────────────────────────────────
  _buildListHTML(countries, instant) {
    if (countries.length === 0)
      return '<div class="cs-empty">No matches</div>';

    return countries.map(c => {
      const active   = c.name === this.currentCountry ? 'active' : '';
      const pct      = c.primacy > 0 ? (c.primacy * 100).toFixed(0) + '%' : '';
      const barWidth = c.primacy > 0 ? (c.primacy * 100).toFixed(1) : 0;
      const badge    = instant ? '⚡' : '🔄';
      // safe name for onclick — escape single quotes
      const safeName = c.name.replace(/'/g, "\\'");
      return `
        <div class="cs-item ${active}"
             onclick="CountrySwitcher.selectCountry('${safeName}')">
          <div class="cs-item-left">
            <span class="cs-badge">${badge}</span>
            <span class="cs-name">${c.name}</span>
          </div>
          <div class="cs-item-right">
            ${pct ? `<span class="cs-primacy">${pct}</span>` : ''}
            ${c.primacy > 0 ? `
            <div class="cs-bar">
              <div class="cs-bar-fill ${c.pattern}"
                   style="width:${barWidth}%"></div>
            </div>` : ''}
          </div>
        </div>`;
    }).join('');
  },

  // ── Render panel into DOM ─────────────────────────────────────
  _render() {
    const pipelineSection = IS_LOCAL ? `
      <div id="cs-pipeline-section">
        <div class="cs-section-label">🔄 Run Pipeline (any country)</div>
        <div id="cs-pipeline-list"></div>
      </div>` : '';

    const html = `
      <div id="cs-overlay" onclick="CountrySwitcher.close()"></div>
      <div id="cs-panel">
        <div id="cs-header">
          <span>🌍 Switch Country</span>
          <button class="cs-close-btn" onclick="CountrySwitcher.close()">✕</button>
        </div>
        <div id="cs-search-wrap">
          <input id="cs-search" type="text"
                 placeholder="Search ${this.allCountries.length} countries…"
                 oninput="CountrySwitcher.search(this.value)" />
        </div>
        <div id="cs-body">
          <div class="cs-section-label">⚡ Instant Load (pre-generated)</div>
          <div id="cs-pregenerated-list"></div>
          ${pipelineSection}
        </div>
      </div>`;

    document.body.insertAdjacentHTML('beforeend', html);

    // Initial list population
    this.search('');
  },

  // ── Inject trigger button into #header ───────────────────────
  _injectTriggerButton() {
    const header     = document.getElementById('header');
    if (!header) return;

    // Hide legacy countrySelect — CountrySwitcher supersedes it
    const legacySelect = document.getElementById('countrySelect');
    if (legacySelect) legacySelect.style.display = 'none';

    const btn    = document.createElement('button');
    btn.id       = 'cs-trigger';
    btn.innerHTML = '🌍 Select Country ▾';
    btn.onclick   = () => CountrySwitcher.open();

    // Insert before .toggle-wrap so it sits between status and toggles
    const toggleWrap = header.querySelector('.toggle-wrap');
    if (toggleWrap) {
      header.insertBefore(btn, toggleWrap);
    } else {
      header.appendChild(btn);
    }
  },

  // ── Update trigger button label ───────────────────────────────
  _updateTrigger(name) {
    const btn = document.getElementById('cs-trigger');
    if (btn) btn.innerHTML = `🌍 ${name} ▾`;
  },
};

// nav.js — Shared navigation (Prompt 18)
// Loaded by every page. Call Nav.init() or Nav.augmentHeader() as appropriate.

const Nav = {

  pages: [
    { label: 'Explore',        href: 'index.html'   },
    { label: 'Global Ranking', href: 'ranking.html' },
  ],

  currentPage() {
    return window.location.pathname.split('/').pop() || 'landing.html';
  },

  // ── Full standalone nav — use on landing.html ───────────────────
  init(options = {}) {
    const theme   = options.theme || 'solid';
    const current = this.currentPage();

    const nav = document.createElement('nav');
    nav.id        = 'global-nav';
    nav.className = `nav-${theme}`;
    nav.innerHTML = `
      <a href="landing.html" class="nav-brand">🌍 <span>Urban Gravity</span></a>
      <div class="nav-links">
        ${this.pages.map(p => `
          <a href="${p.href}" class="nav-link ${current === p.href ? 'active' : ''}">
            ${p.label}
          </a>`).join('')}
        <button class="nav-link" onclick="Nav.openAbout()">About</button>
      </div>`;

    document.body.insertAdjacentElement('afterbegin', nav);

    // push page content down on solid pages
    if (theme === 'solid') {
      document.body.style.paddingTop = '52px';
    }

    this._injectAboutPanel();
  },

  // ── Augment existing header — use on index.html & ranking.html ──
  // Prepends a home brand link and appends an About button to #header
  augmentHeader() {
    const header = document.getElementById('header');
    if (!header) { this.init(); return; }

    // Brand link — home
    const brand = document.createElement('a');
    brand.href      = 'landing.html';
    brand.className = 'hdr-brand';
    brand.title     = 'Back to home';
    brand.textContent = '🌍 Home';
    header.insertAdjacentElement('afterbegin', brand);

    // About button — appended at the end
    const aboutBtn = document.createElement('button');
    aboutBtn.className   = 'nav-about-btn';
    aboutBtn.textContent = 'About';
    aboutBtn.onclick     = () => Nav.openAbout();
    header.appendChild(aboutBtn);

    this._injectAboutPanel();
  },

  // ── About panel ─────────────────────────────────────────────────
  _injectAboutPanel() {
    const overlay = document.createElement('div');
    overlay.id      = 'about-overlay';
    overlay.onclick = () => Nav.closeAbout();

    const panel = document.createElement('div');
    panel.id        = 'about-panel';
    panel.innerHTML = `
      <button id="about-close" onclick="Nav.closeAbout()">✕</button>

      <div class="about-title">Urban Gravity</div>
      <div class="about-subtitle">The physics of human settlement, made visible.</div>

      <div class="about-section">What this is</div>
      <p>An interactive data platform that applies Newton's gravitational model to
      43,645 cities across 191 countries. Cities are treated as masses — larger cities
      attract more strongly, distance weakens the pull by its square.</p>

      <div class="about-section">Why it's interesting</div>
      <p>The same mathematics that governs planetary orbits predicts trade flows,
      migration patterns, and economic connections between cities. This project makes
      that invisible physics visible — and lets you explore it for any country in
      the world.</p>

      <div class="about-section">What was built</div>
      <p>A full data pipeline (Python + Bash) processes raw CSV data into gravity
      networks and concentration reports. D3.js v7 renders the results as animated
      SVG overlaid on a Leaflet map. A global ranking choropleth covers 191 countries
      computed in a single batch run.</p>

      <div class="about-tech">
        <span>D3.js v7</span>
        <span>Leaflet.js</span>
        <span>Python</span>
        <span>pandas</span>
        <span>Newton Gravity Model</span>
        <span>Haversine Formula</span>
        <span>43,645 cities</span>
      </div>

      <a href="https://github.com/Yadav108/world-cities-explorer"
         target="_blank" rel="noopener" class="about-github">
        View on GitHub →
      </a>`;

    document.body.appendChild(overlay);
    document.body.appendChild(panel);
  },

  openAbout() {
    document.getElementById('about-overlay').classList.add('open');
    document.getElementById('about-panel').classList.add('open');
  },

  closeAbout() {
    document.getElementById('about-overlay').classList.remove('open');
    document.getElementById('about-panel').classList.remove('open');
  },
};

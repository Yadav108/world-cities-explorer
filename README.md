# 🌍 World Cities Explorer

An interactive, population-scaled world cities map built with **D3.js v7 + Leaflet.js**, powered by a **Bash/Python data pipeline** processing 43,000+ cities globally.

> Built as part of a Computer Science data processing pipeline project — from raw CSV to interactive browser visualization, with zero backend dependencies.

---

## 🖥️ Live Demo

🔗 [world-cities-explorer](https://github.com/Yadav108/world-cities-explorer)

---

## 🏗️ Architecture

```
worldcities.csv (43K rows)
       │
       ├──▶ pipeline.py / pipeline.sh   ← pre-filter → cities.json
       │
       └──▶ index.html  ←── d3.csv() loads CSV directly in browser
                              │
                    ┌─────────┴──────────┐
               Leaflet.js           D3.js v7
              (tile basemap)    (SVG circles overlay)
```

---

## ✨ Features

### 🗺️ Interactive Map
- Dark CartoDB basemap with D3 SVG circles overlaid via Leaflet's `L.svg()` layer
- Population-scaled circles using `d3.scaleSqrt()` — prevents large cities from dominating
- Color gradient via `d3.interpolateYlOrRd` (yellow → red by population)
- Capital city markers highlighted with white stroke ring
- Zoom-based culling — only cities >1M shown at world zoom; reveals more on zoom-in
- Smooth enter/exit transitions when switching countries

### 🔍 Search & Navigation
- Autocomplete dropdown with keyboard navigation (↑ ↓ Enter Esc)
- Instant country switching — CSV loaded once in memory, no re-pipeline needed
- City highlight search — matching circle pulses on the map
- Auto-fit bounds — map zooms to fit selected country

### ⚖️ Compare Mode
- Side-by-side overlay of two countries on the same map
- Country A: `YlOrRd` scale (cyan accent)
- Country B: `BuPu` scale (orange accent)
- Tooltip shows colored dot + country label in compare mode

### 🎚️ Population Filter
- Slider with power-curve scaling (`val^2.5`) for resolution at low populations
- Live filtering — drag to remove circles below threshold instantly
- Combines with zoom-level culling

### 📊 Stats Panel
- City count, total population, largest city, capital name
- Population scale legend with 5 color-coded steps
- Scrollable cities list sorted by population — click any to pan the map

---

## 🛠️ Tech Stack

| Tool | Version | Role |
|---|---|---|
| Leaflet.js | 1.9.4 | Tile basemap + SVG layer host |
| D3.js | v7 | Data binding, scales, transitions, SVG |
| pandas | 2.x | CSV processing in Python pipeline |
| awk / bash | — | Bash pipeline for filtering |
| Python http.server | built-in | Local development server |

---

## 📁 File Structure

```
world-cities-explorer/
├── index.html          # Main app — interactive map UI
├── pipeline.py         # Python data pipeline (Windows-native)
├── pipeline.sh         # Bash data pipeline (Git Bash / WSL)
├── worldcities.csv     # Source dataset — 43,645 cities globally
├── cities.json         # Pipeline output — filtered country subset
├── .gitignore
└── README.md
```

---

## 🚀 How to Run

### 1. Get the dataset
Download `worldcities.csv` from [SimpleMaps](https://simplemaps.com/data/world-cities) and place it in the project root.

### 2. Start local server
```bash
cd world-cities-explorer
python -m http.server 8080
```

### 3. Open in browser
```
http://localhost:8080
```

### 4. Explore
Type any country → press **Enter** or click **Explore**
```
Examples: Germany · India · Japan · Brazil · United States
```

### Optional: Pre-generate cities.json via pipeline
```bash
# Windows (PyCharm terminal)
python pipeline.py

# Git Bash / WSL
bash pipeline.sh
```

---

## 🧠 Key Design Decisions

**Why `d3.scaleSqrt()` for radius?**
Population values span 4 orders of magnitude (50K → 38M). Linear scaling makes small cities invisible. Square root compression keeps all cities visually meaningful.

**Why D3 over Folium?**
Folium generates static HTML. D3 gives direct control over every SVG element — enabling live transitions, compare mode, and zoom-based culling that Folium cannot do.

**Why Leaflet + D3 together?**
Leaflet handles tile loading and map interaction. D3 handles data-to-visual binding. Together they cover what neither does alone.

---

## 📊 Dataset

- **Source:** [SimpleMaps World Cities Basic](https://simplemaps.com/data/world-cities)
- **Size:** 43,645 cities across 233 countries
- **Fields used:** `city`, `lat`, `lng`, `country`, `population`, `capital`

---

## 👤 Author

**Aryan Yadav**
Mechatronics Engineering Student — THWS, Germany
[GitHub: Yadav108](https://github.com/Yadav108)

---

## 📄 License
MIT

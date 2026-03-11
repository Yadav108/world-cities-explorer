# 🌍 World Cities Explorer

An interactive map that lets you explore cities of any country in the world — with population data visualised as colour-coded circles on a dark Leaflet + D3.js map.

![World Cities Explorer](https://img.shields.io/badge/D3.js-v7-orange) ![Leaflet](https://img.shields.io/badge/Leaflet-1.9.4-green) ![Python](https://img.shields.io/badge/Python-3.x-blue)

---

## ✨ Features

- 🔍 **Live country search** with autocomplete dropdown — switch countries instantly, no reload needed
- 🗺️ **Interactive dark map** (CartoDB Dark Matter tiles) with zoom, pan, and scroll
- 📊 **Population circles** — size and colour scaled with `d3.scaleSqrt` + `YlOrRd` palette
- 🔢 **Population labels** on circles, visible when zoomed in (zoom ≥ 5)
- 🏛️ **Capital cities** highlighted with a white stroke
- 🖱️ **Hover tooltips** showing city name, population, and capital status
- 📋 **Full cities list** in the right panel — all cities sorted by population

---

## 🚀 Quick Start

### Option A — Browse directly (no pipeline needed)

The app loads `worldcities.csv` directly in the browser.

```bash
# 1. Start local server (required for file access)
python -m http.server 8080

# 2. Open browser
http://localhost:8080

# 3. Type any country name → press Enter or click Explore
```

### Option B — Pre-filter with the pipeline

Use this if you want a lightweight `cities.json` for a specific country.

```bash
# Python (Windows / any OS)
python pipeline.py

# Bash (Git Bash / Linux / macOS)
bash pipeline.sh
```

Then start the server and open the browser as above.

---

## 📁 File Structure

```
world-cities-explorer/
├── worldcities.csv       ← Dataset (from simplemaps.com/data/world-cities)
├── index.html            ← D3 + Leaflet interactive map (main app)
├── pipeline.py           ← Python data pipeline (generates cities.json)
├── pipeline.sh           ← Bash data pipeline (generates cities.json)
└── README.md
```

---

## 📦 Dataset

- **Source:** [SimpleMaps World Cities Database](https://simplemaps.com/data/world-cities) (free tier)
- **File:** `worldcities.csv`
- **Size:** ~43,000 cities across 200+ countries
- **Columns used:** `city`, `lat`, `lng`, `country`, `population`, `capital`

---

## 🛠️ Dependencies

| Tool | Version | Purpose |
|---|---|---|
| [Leaflet.js](https://leafletjs.com/) | 1.9.4 | Tile map base layer |
| [D3.js](https://d3js.org/) | v7 | Data binding + SVG circles |
| [pandas](https://pandas.pydata.org/) | latest | Python CSV processing (pipeline only) |
| Python `http.server` | built-in | Local dev server |

---

## 🖼️ How It Works

1. On page load, `worldcities.csv` is fetched and parsed entirely in the browser with `d3.csv()`
2. All ~43K city records are held in memory
3. When you type a country name, the data is filtered client-side in milliseconds
4. D3 binds the filtered data to SVG `<circle>` elements overlaid on the Leaflet map via `L.svg()`
5. On every zoom/pan event, circles are reprojected using `map.latLngToLayerPoint()`

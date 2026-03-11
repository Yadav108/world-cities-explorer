## Why does Bangkok hold 58% of Thailand's urban population?
## Why is Germany's city network so different from France's?

These questions have a mathematical answer.

Newton's gravitational law — the same equation governing planetary orbits — predicts the attraction between cities with remarkable accuracy. Larger cities pull harder. Distance weakens the pull by its square. The result is a measurable, visualizable network of urban gravity.

This project makes that network visible for **191 countries** and **43,645 cities**.

---

## 🔗 Live Demo

**[yadav108.github.io/world-cities-explorer](https://yadav108.github.io/world-cities-explorer/)**

> Select any of 30 pre-generated countries for instant analysis.  
> Running locally unlocks the dynamic pipeline for all 191 countries.

---

## What It Does

### ⚡ Gravity Network
Every country's top 10 cities are modeled as gravitational masses. The attraction between each pair is calculated using Newton's formula, normalized, and rendered as animated SVG lines — thickness and pulse speed proportional to gravitational strength.

```
gravity(A, B) = (pop_A × pop_B) / distance_km²
```

A Rhine-Ruhr cluster (Cologne ↔ Düsseldorf, 26 km apart) dominates Germany. Tokyo ↔ Yokohama dominates Japan. The formula finds these without being told.

### 📊 Primacy Index
A single number measuring urban concentration:

```
P = Population_largest / Σ Population_all_cities
```

| Value | Category | Example |
|---|---|---|
| < 0.15 | Distributed | Germany, USA |
| 0.15–0.35 | Moderate | Italy, Vietnam |
| > 0.35 | Dominant | Thailand, Argentina |

### 🌍 Global Ranking
All 191 countries computed in a single batch run and rendered as a D3 choropleth. Click any country to load its full gravity + concentration analysis instantly.

### 📐 Math Transparency
Every number is explainable on demand. Click **Show Math** next to any result to expand the exact calculation with real values substituted into the formula — primacy index, Newton gravity, and Haversine distance.

---

## Key Technical Decisions

**Why D3.js over Folium or Matplotlib?**  
Folium generates static HTML with no interactivity beyond basic tooltips. D3 gives direct access to every SVG element — enabling live transitions, zoom-aware reprojection, and animated gravity pulses that update on every map event. The tradeoff is complexity; the payoff is a visualization that responds to data rather than just displaying it.

**Why square root scaling for circle radius?**  
Population values span four orders of magnitude — from 50,000 to 38,000,000. Linear scaling makes small cities invisible. `d3.scaleSqrt()` compresses the range while preserving relative differences, keeping all cities visually meaningful.

**Why Haversine over Euclidean distance?**  
Straight-line distance between lat/lng coordinates ignores Earth's curvature. For cities 500 km apart, Euclidean distance underestimates by ~15 km — enough to meaningfully distort gravity scores. Haversine gives the true great-circle distance.

**Why normalize gravity scores?**  
Raw gravity scores depend entirely on population scale. Germany's raw scores are millions of times larger than Luxembourg's — not because the network is stronger, but because the populations are larger. Min-max normalization makes scores comparable within any country regardless of absolute population size.

**Why filter pairs below 0.15?**  
At 10 cities, there are 45 possible pairs. Drawing all of them creates visual noise that obscures the actual network structure. The 0.15 threshold retains the gravitationally significant connections while eliminating weak long-distance pairs that add clutter without insight.

**Why pre-generate 30 countries for deployment?**  
GitHub Pages serves static files only — no Python runtime. Pre-generating the 30 most populated countries covers ~85% of likely user queries while keeping the repo size manageable. The local server mode preserves full dynamic pipeline access for all 191 countries.

---

## Architecture

```
worldcities.csv (43,645 rows)
        │
        ├── generate_gravity.py
        │     ├── Haversine distance calculation
        │     ├── Newton gravity scoring + normalization
        │     ├── Primacy Index + confidence bands
        │     ├── InsightNarrator (rule-based pattern recognition)
        │     └── Batch export → data/{Country}/
        │
        ├── server.py
        │     └── /run-pipeline?country=X → subprocess → JSON
        │
        └── Browser
              ├── landing.html       → entry point + animated background
              ├── index.html         → D3 + Leaflet unified app
              │     ├── Gravity mode: SVG lines + pulse animation
              │     ├── Concentration mode: arc gauge + bar chart
              │     ├── NL query: Transformers.js zero-shot classifier
              │     ├── Math transparency: inline formula expansion
              │     └── Country switcher: instant or pipeline load
              └── ranking.html       → D3 choropleth, 191 countries
```

---

## Tech Stack

| Layer | Tool | Why |
|---|---|---|
| Map rendering | Leaflet.js 1.9.4 | Tile loading + SVG layer host |
| Data visualization | D3.js v7 | Direct SVG binding, transitions, scales |
| Data pipeline | Python + pandas | CSV processing, batch generation |
| Geographic distance | Haversine (custom) | Great-circle accuracy |
| Gravity model | Newton (custom) | Spatial interaction modeling |
| NL query | Transformers.js 2.17 | Zero-shot classification, runs in-browser |
| Local server | Python http.server | Static files + `/run-pipeline` API |
| Deployment | GitHub Pages | Zero-server static hosting |

---

## How to Run

### Prerequisites
```bash
pip install pandas
```

### Local — full dynamic mode (all 191 countries)
```bash
git clone https://github.com/Yadav108/world-cities-explorer
cd world-cities-explorer

# Download dataset → https://simplemaps.com/data/world-cities
# Place worldcities.csv in project root

python server.py
# → http://localhost:8000
```

Use the **🌍 Select Country** button to switch between any of 191 countries. The pipeline runs server-side and updates the visualization in ~2 seconds.

### Pre-generate data for deployment
```bash
python generate_gravity.py --batch
# Creates data/{Country}/ for 30 countries
# Commit data/ folder to repo → GitHub Pages serves it statically
```

### API endpoint (local only)
```
GET /run-pipeline?country=Japan
→ runs generate_gravity.py Japan
→ returns { "status": "ok", "country": "Japan" }
```

---

## File Structure

```
world-cities-explorer/
├── landing.html              ← entry point
├── index.html                ← main app (gravity + concentration + NL)
├── ranking.html              ← global choropleth
├── nav.js / nav.css          ← shared navigation + About panel
├── country-switcher.js       ← country switcher panel
├── generate_gravity.py       ← master pipeline + batch generator
├── server.py                 ← dev server with pipeline API
├── pipeline.py               ← simple CSV filter (original)
├── world.geojson             ← 191-country boundaries
├── global_ranking.json       ← pre-computed primacy for all countries
└── data/
    ├── Germany/
    │   ├── gravity_data.json
    │   └── concentration.json
    └── ... (29 more countries)
```

---

## Example NL Queries

Type anything in the query bar — the hybrid classifier handles it:

| Query | Intent | Method |
|---|---|---|
| `gravity network in Japan` | gravity · Japan | keyword |
| `which city dominates France?` | concentration · France | keyword |
| `how distributed is Germany` | concentration · Germany | keyword |
| `urban hierarchy in Thailand` | concentration · Thailand | keyword |
| `paris vs rest of france` | concentration · France | ML model |
| `connections between Indian cities` | gravity · India | keyword |

Keyword matching is instant. The ML model (Transformers.js `nli-deberta-v3-small`, ~20 MB) loads once and is cached in the browser permanently.

---

## Data

[SimpleMaps World Cities Basic](https://simplemaps.com/data/world-cities)  
43,645 cities · 233 countries · Free for personal and commercial use

`worldcities.csv` is excluded from the repo (`.gitignore`) — download it directly from SimpleMaps and place it at the project root before running the pipeline locally.

---

## Author

**Aryan Yadav**  
Mechatronics Engineering — THWS Würzburg-Schweinfurt, Germany

Interests: data visualization, spatial modeling, explainable AI, autonomous systems.

[GitHub](https://github.com/Yadav108)

---

## License

MIT


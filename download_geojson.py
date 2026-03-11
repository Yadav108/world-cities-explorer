"""
download_geojson.py — Run once to fetch world country boundary polygons.

Usage:
    python download_geojson.py

Saves: world.geojson  (~500 KB, Natural Earth via holtzy/D3-graph-gallery)
"""

import urllib.request
import json
import os

URL  = "https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world.geojson"
DEST = "world.geojson"

if os.path.exists(DEST):
    print(f"✅  '{DEST}' already exists — delete it to re-download.")
else:
    print(f"Downloading {URL} …")
    try:
        with urllib.request.urlopen(URL, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        with open(DEST, "w", encoding="utf-8") as f:
            json.dump(data, f)

        n_features = len(data.get("features", []))
        print(f"✅  Saved '{DEST}'  ({n_features} country features)")

        # Show first 5 country names so you can verify the property key
        names = [ft["properties"].get("name", "?") for ft in data["features"][:5]]
        print(f"    Sample names: {names}")

    except Exception as e:
        print(f"❌  Download failed: {e}")
        print("    Try manually saving the URL above as 'world.geojson'")

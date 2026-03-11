"""
pipeline.py — Filter worldcities.csv by country and output cities.json
Python fallback for Windows users (no Bash required).
"""

import json
import sys
import os

try:
    import pandas as pd
except ImportError:
    print("Error: pandas is not installed.")
    print("Run:  pip install pandas")
    sys.exit(1)

INPUT_FILE = "worldcities.csv"
OUTPUT_FILE = "cities.json"

print("=" * 44)
print("  World Cities Data Pipeline (Python)")
print("=" * 44)
print()

# ── Load CSV ──────────────────────────────────────────
if not os.path.exists(INPUT_FILE):
    print(f"Error: '{INPUT_FILE}' not found in current directory.")
    sys.exit(1)

try:
    df = pd.read_csv(INPUT_FILE, dtype=str, encoding="utf-8")
except Exception as e:
    print(f"Error reading CSV: {e}")
    sys.exit(1)

# Normalise column names (strip whitespace)
df.columns = df.columns.str.strip()

# Required columns
required = {"city", "lat", "lng", "country", "population", "capital"}
missing_cols = required - set(df.columns)
if missing_cols:
    print(f"Error: Missing columns in CSV: {missing_cols}")
    print(f"Available columns: {list(df.columns)}")
    sys.exit(1)

# ── Ask for country ───────────────────────────────────
country_input = input("Enter country name: ").strip()
if not country_input:
    print("Error: Country name cannot be empty.")
    sys.exit(1)

print(f"\nProcessing '{country_input}'...")

# ── Filter ────────────────────────────────────────────
mask = df["country"].str.lower() == country_input.lower()
filtered = df[mask].copy()

# If no exact match, suggest partial matches
if filtered.empty:
    partial_mask = df["country"].str.lower().str.contains(country_input.lower(), na=False)
    partial = df[partial_mask]["country"].unique()

    print(f"\n⚠  No exact match found for '{country_input}'.")
    if len(partial) > 0:
        print("   Did you mean one of these?")
        for name in sorted(partial)[:10]:
            print(f"     • {name}")
    else:
        print("   No partial matches found either. Check spelling.")
    sys.exit(1)

# ── Clean data ────────────────────────────────────────
# Drop rows with missing lat/lng
filtered = filtered.dropna(subset=["lat", "lng"])
filtered = filtered[filtered["lat"].str.strip() != ""]
filtered = filtered[filtered["lng"].str.strip() != ""]

# Convert lat/lng to float
filtered["lat"] = pd.to_numeric(filtered["lat"], errors="coerce")
filtered["lng"] = pd.to_numeric(filtered["lng"], errors="coerce")
filtered = filtered.dropna(subset=["lat", "lng"])

# Handle missing population → default 0
filtered["population"] = pd.to_numeric(filtered["population"], errors="coerce").fillna(0).astype(int)

# Normalise capital field
filtered["capital"] = filtered["capital"].fillna("").str.strip()

# ── Build JSON ────────────────────────────────────────
records = []
for _, row in filtered.iterrows():
    records.append({
        "city":       str(row["city"]).strip(),
        "lat":        round(float(row["lat"]), 6),
        "lng":        round(float(row["lng"]), 6),
        "population": int(row["population"]),
        "capital":    str(row["capital"]),
    })

# Sort by population descending (optional, nice for the map)
records.sort(key=lambda x: x["population"], reverse=True)

# ── Write output ──────────────────────────────────────
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(records, f, indent=2, ensure_ascii=False)

print(f"\n✅ Found {len(records)} cities for '{country_input}'")
print(f"   Saved to {OUTPUT_FILE}")
print()
print("-" * 44)
print("  Next steps:")
print("    python -m http.server 8080")
print("    Then open: http://localhost:8080")
print("-" * 44)

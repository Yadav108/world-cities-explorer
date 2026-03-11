"""
pipeline.py — Filter worldcities.csv by country and output cities.json
Python fallback for Windows users (no Bash required).
"""

import json
import sys
import os
import time

try:
    import pandas as pd
except ImportError:
    print("❌  pandas is not installed.")
    print("    Fix: pip install pandas")
    sys.exit(1)

INPUT_FILE  = "worldcities.csv"
OUTPUT_FILE = "cities.json"

print("=" * 48)
print("  World Cities Data Pipeline (Python)")
print("=" * 48)
print()

# ── Load CSV ──────────────────────────────────────────
if not os.path.exists(INPUT_FILE):
    print(f"❌  '{INPUT_FILE}' not found in: {os.getcwd()}")
    print("    Download it from: https://simplemaps.com/data/world-cities")
    sys.exit(1)

t0 = time.time()
df = None

# Try multiple encodings — simplemaps files sometimes ship with BOM
for enc in ("utf-8-sig", "utf-8", "latin-1"):
    try:
        df = pd.read_csv(INPUT_FILE, dtype=str, encoding=enc)
        break
    except UnicodeDecodeError:
        continue
    except Exception as e:
        print(f"❌  Failed to read CSV: {e}")
        sys.exit(1)

if df is None:
    print("❌  Could not decode CSV — try opening it in a text editor and saving as UTF-8.")
    sys.exit(1)

# Normalise column names
df.columns = df.columns.str.strip().str.lower()

required = {"city", "lat", "lng", "country", "population", "capital"}
missing  = required - set(df.columns)
if missing:
    print(f"❌  Missing columns in CSV: {missing}")
    print(f"    Available columns: {list(df.columns)}")
    sys.exit(1)

print(f"    Loaded {len(df):,} rows  ({time.time() - t0:.1f}s)")

# ── Ask for country ───────────────────────────────────
country_input = input("\nEnter country name: ").strip()
if not country_input:
    print("❌  Country name cannot be empty.")
    sys.exit(1)

print(f"\nProcessing '{country_input}'…")

# ── Exact match ───────────────────────────────────────
mask     = df["country"].str.strip().str.lower() == country_input.lower()
filtered = df[mask].copy()

if filtered.empty:
    # Fuzzy hint: find partial matches so user can correct spelling
    partial_mask = df["country"].str.lower().str.contains(
        country_input.lower(), na=False, regex=False
    )
    partials = sorted(df[partial_mask]["country"].dropna().unique())

    print(f"\n⚠️   No exact match for '{country_input}'.")
    if partials:
        print("    Did you mean one of these?")
        for name in partials[:10]:
            print(f"      • {name}")
    else:
        print("    No partial matches either. Check spelling.")
    sys.exit(1)

# ── Clean coordinates ─────────────────────────────────
before = len(filtered)

# Drop rows that are missing or blank in lat/lng
filtered = filtered.dropna(subset=["lat", "lng"])
filtered = filtered[
    filtered["lat"].str.strip().ne("") &
    filtered["lng"].str.strip().ne("")
]

# Convert to float — rows that can't be parsed become NaN and are dropped
filtered["lat"] = pd.to_numeric(filtered["lat"], errors="coerce")
filtered["lng"] = pd.to_numeric(filtered["lng"], errors="coerce")
filtered = filtered.dropna(subset=["lat", "lng"])

dropped = before - len(filtered)
if dropped:
    print(f"    (Skipped {dropped} rows with invalid/missing coordinates)")

if filtered.empty:
    print(f"❌  No valid rows remain after cleaning for '{country_input}'.")
    sys.exit(1)

# ── Clean population ──────────────────────────────────
filtered["population"] = (
    pd.to_numeric(filtered["population"], errors="coerce")
    .fillna(0)
    .clip(lower=0)   # no negative populations
    .astype(int)
)

no_pop = (filtered["population"] == 0).sum()
if no_pop:
    print(f"    (Note: {no_pop} cities have no population data — stored as 0)")

# ── Normalise capital field ───────────────────────────
filtered["capital"] = filtered["capital"].fillna("").str.strip().str.lower()

# ── Build JSON records ────────────────────────────────
records = [
    {
        "city":       str(row["city"]).strip(),
        "lat":        round(float(row["lat"]),  6),
        "lng":        round(float(row["lng"]),  6),
        "population": int(row["population"]),
        "capital":    str(row["capital"]),
    }
    for _, row in filtered.iterrows()
]

# Sort descending by population (matches the in-browser sort)
records.sort(key=lambda x: x["population"], reverse=True)

# ── Write output ──────────────────────────────────────
try:
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)
except OSError as e:
    print(f"❌  Could not write {OUTPUT_FILE}: {e}")
    sys.exit(1)

# ── Summary stats ─────────────────────────────────────
total_pop = sum(r["population"] for r in records)
capital   = next((r for r in records if r["capital"] == "primary"), None)
largest   = records[0] if records else None
country   = filtered.iloc[0]["country"]

print(f"\n✅  {len(records):,} cities exported for '{country}'")
print(f"    Total population : {total_pop:,}")
if largest:
    print(f"    Largest city     : {largest['city']} ({largest['population']:,})")
if capital:
    print(f"    Capital          : {capital['city']}")
else:
    print(f"    Capital          : not found in dataset")
print(f"    Output file      : {OUTPUT_FILE}")
print()
print("-" * 48)
print("  Next steps:")
print("    python -m http.server 8080")
print("    Then open: http://localhost:8080")
print("-" * 48)

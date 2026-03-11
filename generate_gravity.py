"""
generate_gravity.py — Prompts 1–12 end-to-end.
Outputs:
  gravity_data.json     → for gravity network visualization
  concentration.json    → for primacy index visualization (+ narration block)
  global_ranking.json   → for world choropleth (Prompt 12)

Usage:
  python generate_gravity.py              ← uses built-in Germany dataset
  python generate_gravity.py Japan        ← pulls Japan from worldcities.csv
  python generate_gravity.py "United States"
  python generate_gravity.py global       ← ranks all countries, saves global_ranking.json
"""

import math
import json
import sys
from datetime import date
from itertools import combinations

# Force UTF-8 stdout on Windows (avoids cp1252 emoji encoding errors)
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# ── Prompt 12: GeoJSON name mapping ──────────────────────────────────────────
# Maps worldcities.csv country names → Natural Earth GeoJSON names (holtzy/D3 gallery)
NAME_MAP = {
    "United States":              "United States of America",
    "Czech Republic":             "Czech Rep.",
    "Bosnia and Herzegovina":     "Bosnia and Herz.",
    "Central African Republic":   "Central African Rep.",
    "Dominican Republic":         "Dominican Rep.",
    "South Sudan":                "S. Sudan",
    "Ivory Coast":                "Côte d'Ivoire",
    "Tanzania":                   "United Rep. of Tanzania",
    "North Korea":                "Dem. Rep. Korea",
    "South Korea":                "Republic of Korea",
    "Syria":                      "Syrian Arab Republic",
    "Russia":                     "Russian Federation",
    "Bolivia":                    "Bolivia (Plurin. State of)",
    "Venezuela":                  "Venezuela (Bol. Rep. of)",
    "Iran":                       "Iran (Islamic Rep. of)",
    "Moldova":                    "Republic of Moldova",
    "Taiwan":                     "Taiwan",
    "Palestine":                  "State of Palestine",
    "Laos":                       "Lao People's Dem. Rep.",
    "Vietnam":                    "Viet Nam",
    "Myanmar":                    "Myanmar",
    "Congo":                      "Congo",
    "Serbia":                     "Serbia",
}

# ── Prompt 1: Haversine ───────────────────────────────────────────────────────
def haversine(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    R = 6371
    lat1, lng1, lat2, lng2 = map(math.radians, [lat1, lng1, lat2, lng2])
    dlat = lat2 - lat1
    dlng = lng2 - lng1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlng / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


# ── Prompt 2: Gravity Score Calculator ───────────────────────────────────────
def calculate_gravity_pairs(cities: list[dict]) -> list[dict]:
    top10 = sorted(cities, key=lambda c: c["population"], reverse=True)[:10]

    raw_pairs = []
    for a, b in combinations(top10, 2):
        dist = haversine(a["lat"], a["lng"], b["lat"], b["lng"])
        if dist == 0:
            continue
        raw_gravity = (a["population"] * b["population"]) / dist ** 2
        raw_pairs.append({
            "city_a":      a["city"],
            "city_b":      b["city"],
            "distance_km": round(dist, 1),
            "raw_gravity": raw_gravity,
            "pop_a":       a["population"],
            "pop_b":       b["population"],
        })

    max_g = max(p["raw_gravity"] for p in raw_pairs)
    min_g = min(p["raw_gravity"] for p in raw_pairs)
    span  = max_g - min_g or 1

    for p in raw_pairs:
        p["gravity"] = round((p["raw_gravity"] - min_g) / span, 4)

    result = [p for p in raw_pairs if p["gravity"] >= 0.15]
    result.sort(key=lambda p: p["gravity"], reverse=True)

    for p in result:
        del p["raw_gravity"]

    return result


# ── Prompt 3: JSON Export ─────────────────────────────────────────────────────
def export_for_d3(cities: list[dict], pairs: list[dict], country: str,
                  path: str = "gravity_data.json") -> None:
    top10       = sorted(cities, key=lambda c: c["population"], reverse=True)[:10]
    city_lookup = {c["city"]: c for c in top10}

    ranked_cities = [
        {
            "city":       c["city"],
            "lat":        c["lat"],
            "lng":        c["lng"],
            "population": c["population"],
            "rank":       rank,
        }
        for rank, c in enumerate(top10, start=1)
    ]

    enriched_pairs = []
    for p in pairs:
        a = city_lookup.get(p["city_a"])
        b = city_lookup.get(p["city_b"])
        if not a or not b:
            continue
        enriched_pairs.append({
            "city_a":      p["city_a"],
            "city_b":      p["city_b"],
            "distance_km": p["distance_km"],
            "gravity":     p["gravity"],
            "pop_a":       p["pop_a"],
            "pop_b":       p["pop_b"],
            "lat_a":       a["lat"],
            "lng_a":       a["lng"],
            "lat_b":       b["lat"],
            "lng_b":       b["lng"],
        })

    strongest = enriched_pairs[0] if enriched_pairs else {}
    meta = {
        "total_cities":   len(ranked_cities),
        "total_pairs":    len(enriched_pairs),
        "strongest_pair": f"{strongest.get('city_a')} → {strongest.get('city_b')}" if strongest else "N/A",
        "generated_at":   date.today().isoformat(),
    }

    payload = {
        "country": country,
        "cities":  ranked_cities,
        "pairs":   enriched_pairs,
        "meta":    meta,
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    print(f"    Saved: {path}  ({meta['total_cities']} cities, {meta['total_pairs']} pairs)")



# ── Prompt 6: Concentration Engine ───────────────────────────────────────────
def calculate_concentration(cities: list[dict], country: str) -> dict:
    """Calculates urban concentration metrics for a country (full city list)."""
    valid     = [c for c in cities if c.get("population", 0) > 0]
    n         = len(valid)
    total_pop = sum(c["population"] for c in valid)

    if n > 15:
        confidence, confidence_note = "high", ""
    elif n >= 5:
        confidence = "medium"
        confidence_note = f"Only {n} cities with population data — index may understate concentration."
    else:
        confidence = "low"
        confidence_note = f"Only {n} cities with population data — primacy index is unreliable."

    ranked        = sorted(valid, key=lambda c: c["population"], reverse=True)
    primacy_index = round(ranked[0]["population"] / total_pop, 4) if total_pop else 0

    top5 = [
        {
            "rank":       i + 1,
            "city":       c["city"],
            "population": c["population"],
            "share_pct":  round(c["population"] / total_pop * 100, 1),
        }
        for i, c in enumerate(ranked[:5])
    ]

    return {
        "country":            country,
        "total_cities":       n,
        "total_population":   total_pop,
        "primacy_index":      primacy_index,
        "confidence":         confidence,
        "confidence_note":    confidence_note,
        "largest_city": {
            "city":       ranked[0]["city"],
            "population": ranked[0]["population"],
            "share_pct":  round(ranked[0]["population"] / total_pop * 100, 1),
        },
        "top5":               top5,
        "top5_combined_share": round(sum(c["share_pct"] for c in top5), 1),
    }


def export_concentration(report: dict, path: str = "concentration.json") -> None:
    """Saves concentration JSON (or custom path) for the UI to read."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    label = {"high": "High", "medium": "Medium", "low": "Low"}.get(report["confidence"], "?")
    print(f"    Saved: {path}  (primacy={report['primacy_index']}, confidence={label})")


# ── Prompt 10: Insight Narration Engine ──────────────────────────────────────
class InsightNarrator:
    """
    Translates raw numeric concentration and gravity outputs into
    human-readable insight sentences using urban geography rules.
    """

    # ── Concentration Narration ───────────────────────────────────────────────
    def narrate_concentration(self, report: dict) -> dict:
        p       = report["primacy_index"]
        city    = report["largest_city"]["city"]
        share   = report["largest_city"]["share_pct"]
        total   = report["total_cities"]
        country = report["country"]
        conf    = report["confidence"]

        if p < 0.15:
            headline = "Highly distributed urban network"
            pattern  = "polycentric"
            similar  = "United States, Germany, Switzerland"
            contrast = "France, Thailand, Argentina"
            body = (
                f"No single city overwhelms {country}'s urban landscape. "
                f"{city} holds {share}% of tracked urban population across {total} cities — "
                f"characteristic of federal or historically polycentric countries "
                f"with multiple strong economic centers."
            )
        elif p < 0.25:
            headline = "Moderately concentrated — one leading city"
            pattern  = "transitional"
            similar  = "United Kingdom, Italy, Canada"
            contrast = "USA, Japan (more distributed) or Thailand, Argentina (more dominant)"
            body = (
                f"{city} leads {country}'s urban system with {share}% of tracked urban population "
                f"across {total} cities — significant but not overwhelming. "
                f"Secondary cities retain meaningful economic weight alongside the capital."
            )
        elif p < 0.35:
            headline = "Strong urban primacy — capital drives the country"
            pattern  = "monocentric"
            similar  = "France, Mexico, South Korea"
            contrast = "Germany, Switzerland (distributed)"
            body = (
                f"{city} dominates {country}'s urban hierarchy with {share}% of tracked urban "
                f"population across {total} cities. The gap between {city} and the second city "
                f"is substantial, reflecting a historically centralised national structure."
            )
        else:
            headline = "Primate city dominance — one city overwhelms all others"
            pattern  = "monocentric"
            similar  = "Thailand, Argentina, Peru"
            contrast = "Germany, United States (distributed)"
            body = (
                f"{city} accounts for a striking {share}% of tracked urban population "
                f"across {total} cities in {country}. "
                f"This level of primacy ({p:.0%}) is characteristic of rapidly urbanising or "
                f"historically centralised economies where one city concentrates political, "
                f"economic and cultural power."
            )

        # Append dataset-size caveat
        if total < 10:
            body += (f" ⚠️ Only {total} cities with data — primacy index likely "
                     f"understates true concentration.")
        elif conf == "medium":
            body += (f" (Dataset covers {total} cities; smaller cities may be "
                     f"underrepresented.)")

        insight_confidence = (
            "high"   if conf == "high"   and total >= 15 else
            "medium" if conf == "medium" else
            "low"
        )

        return {
            "headline":           headline,
            "body":               body,
            "comparison":         f"Similar to: {similar}",
            "contrast":           f"Unlike: {contrast}",
            "pattern":            pattern,
            "insight_confidence": insight_confidence,
        }

    # ── Gravity Narration ─────────────────────────────────────────────────────
    def narrate_gravity(self, pairs: list, cities: list) -> dict:
        if not pairs:
            return {
                "headline":          "Insufficient data for gravity analysis",
                "body":              "Not enough city pairs to determine network structure.",
                "top_pair":          "N/A",
                "network_type":      "unknown",
                "avg_distance_top5": 0,
            }

        top5     = pairs[:5]
        avg_dist = round(sum(p["distance_km"] for p in top5) / len(top5), 1)
        top      = pairs[0]
        combined = top["pop_a"] + top["pop_b"]

        if avg_dist < 150:
            network_type = "clustered"
            headline     = f"Dense gravitational cluster — {top['city_a']} & {top['city_b']}"
            network_desc = (
                f"Cities form a tight gravitational cluster with top pairs averaging {avg_dist:.0f} km apart. "
                f"This dense sub-regional network often functions as a single megalopolitan economy."
            )
        elif avg_dist < 400:
            network_type = "linear"
            headline     = f"Linear city corridor — {top['city_a']} to {top['city_b']}"
            network_desc = (
                f"Cities are connected along a corridor averaging {avg_dist:.0f} km between top pairs — "
                f"typical of coastal, river valley, or industrial belt development."
            )
        else:
            network_type = "dispersed"
            headline     = f"Long-distance gravitational poles — {top['city_a']} & {top['city_b']}"
            network_desc = (
                f"Long-distance connections dominate, with top pairs averaging {avg_dist:.0f} km apart — "
                f"characteristic of large countries with geographically separated economic poles."
            )

        body = (
            f"The strongest gravitational pull exists between {top['city_a']} and {top['city_b']} "
            f"({top['distance_km']:.0f} km apart, combined population {combined:,}). "
            f"{network_desc}"
        )

        return {
            "headline":          headline,
            "body":              body,
            "top_pair":          f"{top['city_a']} → {top['city_b']}",
            "network_type":      network_type,
            "avg_distance_top5": avg_dist,
        }

    # ── Combined Narration ────────────────────────────────────────────────────
    def narrate_combined(self, report: dict, pairs: list, cities: list) -> dict:
        conc = self.narrate_concentration(report)
        grav = self.narrate_gravity(pairs, cities)

        country  = report["country"]
        pattern  = conc["pattern"]
        network  = grav["network_type"]
        city     = report["largest_city"]["city"]
        share    = report["largest_city"]["share_pct"]
        primacy  = report["primacy_index"]
        top_pair = grav["top_pair"]
        avg_dist = grav["avg_distance_top5"]
        top      = pairs[0] if pairs else {}

        # Synthesis sentences keyed by (concentration pattern × network type)
        if pattern == "polycentric" and network == "clustered":
            synthesis = (
                f"{country} presents a classic polycentric structure: no primate city, with "
                f"{city} holding just {share}% of tracked urban population. Gravity is strongest "
                f"within a tight sub-regional cluster ({top_pair}, {avg_dist:.0f} km average "
                f"separation) rather than radiating from a single capital — typical of federal "
                f"economies with distributed industrial heritage."
            )
        elif pattern == "polycentric" and network == "linear":
            synthesis = (
                f"{country} shows a distributed urban system with no dominant primate city "
                f"({city} at {share}%), with gravitational connections forming a corridor "
                f"({top_pair}, avg {avg_dist:.0f} km). Urban power is spread across a geographic "
                f"axis rather than concentrated at a single hub."
            )
        elif pattern == "polycentric" and network == "dispersed":
            synthesis = (
                f"{country} has a highly distributed urban system: {city} holds only {share}% "
                f"of tracked population, and the top gravitational pairs span large distances "
                f"(avg {avg_dist:.0f} km). This reflects a large country without a single "
                f"dominant metropolitan core."
            )
        elif pattern == "transitional" and network == "clustered":
            synthesis = (
                f"{country} sits between distributed and dominant: {city} leads with {share}% "
                f"but doesn't overwhelm. Gravity clusters tightly around {top_pair} "
                f"({avg_dist:.0f} km avg) — a strong sub-regional core coexists with the "
                f"national leader, creating a layered urban hierarchy."
            )
        elif pattern == "transitional":
            synthesis = (
                f"{country} shows moderate urban concentration: {city} holds {share}% of "
                f"tracked population — significant but not overwhelming. The gravity network "
                f"({top_pair}, avg {avg_dist:.0f} km) shows secondary cities maintaining real "
                f"economic weight alongside the leading city."
            )
        elif pattern == "monocentric" and primacy > 0.35:
            synthesis = (
                f"{country} exhibits strong primate city dominance: {city} holds {share}% of "
                f"tracked urban population — a striking concentration. The gravity network "
                f"confirms this: connections involving {city} dominate, with {top_pair} among "
                f"secondary links. This pattern is characteristic of historically centralised "
                f"or rapidly urbanising economies."
            )
        else:  # monocentric, 0.25–0.35
            synthesis = (
                f"{country} shows clear urban primacy: {city} accounts for {share}% of tracked "
                f"population. The gravity network ({top_pair}, avg {avg_dist:.0f} km) reinforces "
                f"this — economic mass concentrates in and around the dominant city, with "
                f"secondary cities playing supporting rather than competing roles."
            )

        return {
            "concentration": conc,
            "gravity":       grav,
            "synthesis":     synthesis,
        }


def export_insight(narrative: dict, path: str = "concentration.json") -> None:
    """Appends narration block into concentration.json (or custom path)."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    data["narration"] = narrative
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"    Narration: {narrative['concentration']['pattern']} / {narrative['gravity']['network_type']}")


# ── Prompt 12: Global Ranking ────────────────────────────────────────────────
def compute_global_ranking(csv_path: str = "worldcities.csv") -> list:
    """
    Reads worldcities.csv, computes primacy index for every country,
    filters out unreliable entries, sorts by primacy descending,
    and saves global_ranking.json.
    """
    import csv as csv_mod

    country_cities: dict = {}

    for enc in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            with open(csv_path, encoding=enc, newline="") as f:
                reader = csv_mod.DictReader(f)
                reader.fieldnames = [h.strip().lower() for h in reader.fieldnames]
                for row in reader:
                    cname = row.get("country", "").strip()
                    if not cname:
                        continue
                    try:
                        pop = int(float(row.get("population") or 0))
                    except ValueError:
                        pop = 0
                    city = row.get("city", "").strip()
                    if cname not in country_cities:
                        country_cities[cname] = []
                    country_cities[cname].append({"city": city, "population": pop})
            break
        except UnicodeDecodeError:
            continue

    ranked = []
    for country, cities in country_cities.items():
        valid     = [c for c in cities if c["population"] > 0]
        total_pop = sum(c["population"] for c in valid)

        # Skip unreliable entries
        if len(valid) < 3 or total_pop == 0:
            continue

        sorted_c = sorted(valid, key=lambda c: c["population"], reverse=True)
        largest  = sorted_c[0]
        primacy  = round(largest["population"] / total_pop, 4)

        n = len(valid)
        confidence = "high" if n > 15 else ("medium" if n >= 5 else "low")

        if   primacy < 0.15: pattern = "polycentric"
        elif primacy < 0.25: pattern = "transitional"
        else:                pattern = "monocentric"

        ranked.append({
            "country":          country,
            "primacy_index":    primacy,
            "largest_city":     largest["city"],
            "largest_city_pop": largest["population"],
            "total_cities":     n,
            "total_population": total_pop,
            "pattern":          pattern,
            "confidence":       confidence,
            "geojson_name":     NAME_MAP.get(country, country),
        })

    ranked.sort(key=lambda x: x["primacy_index"], reverse=True)
    for i, r in enumerate(ranked):
        r["rank"] = i + 1

    with open("global_ranking.json", "w", encoding="utf-8") as f:
        json.dump(ranked, f, indent=2, ensure_ascii=False)

    n_ranked  = len(ranked)
    avg_p     = round(sum(r["primacy_index"] for r in ranked) / n_ranked, 3) if n_ranked else 0
    most_dom  = ranked[0]   if ranked else {}
    most_dist = ranked[-1]  if ranked else {}

    print(f"✅  Saved 'global_ranking.json'")
    print(f"    Countries ranked : {n_ranked}")
    print(f"    Most dominant    : {most_dom.get('country')} ({most_dom.get('primacy_index')})")
    print(f"    Most distributed : {most_dist.get('country')} ({most_dist.get('primacy_index')})")
    print(f"    Avg primacy      : {avg_p}")
    print()
    print("  Top 5:")
    for r in ranked[:5]:
        print(f"    #{r['rank']:<4} {r['country']:<30} {r['primacy_index']:.3f}"
              f"  ({r['largest_city']})")
    print("  Bottom 5:")
    for r in ranked[-5:]:
        print(f"    #{r['rank']:<4} {r['country']:<30} {r['primacy_index']:.3f}"
              f"  ({r['largest_city']})")

    return ranked


# ── Run ───────────────────────────────────────────────────────────────────────
germany = [
    {"city": "Berlin",      "lat": 52.52, "lng": 13.40, "population": 3800000},
    {"city": "Hamburg",     "lat": 53.55, "lng": 10.00, "population": 1900000},
    {"city": "Munich",      "lat": 48.13, "lng": 11.58, "population": 1500000},
    {"city": "Cologne",     "lat": 50.93, "lng":  6.96, "population": 1100000},
    {"city": "Frankfurt",   "lat": 50.11, "lng":  8.68, "population":  770000},
    {"city": "Stuttgart",   "lat": 48.77, "lng":  9.18, "population":  640000},
    {"city": "Düsseldorf",  "lat": 51.22, "lng":  6.77, "population":  620000},
    {"city": "Leipzig",     "lat": 51.34, "lng": 12.38, "population":  600000},
    {"city": "Dortmund",    "lat": 51.51, "lng":  7.46, "population":  590000},
    {"city": "Essen",       "lat": 51.46, "lng":  7.01, "population":  580000},
    {"city": "Bremen",      "lat": 53.07, "lng":  8.80, "population":  570000},
    {"city": "Dresden",     "lat": 51.05, "lng": 13.74, "population":  560000},
    {"city": "Hanover",     "lat": 52.37, "lng":  9.73, "population":  540000},
    {"city": "Nuremberg",   "lat": 49.45, "lng": 11.08, "population":  520000},
    {"city": "Duisburg",    "lat": 51.43, "lng":  6.76, "population":  500000},
    {"city": "Bochum",      "lat": 51.48, "lng":  7.22, "population":  365000},
    {"city": "Wuppertal",   "lat": 51.26, "lng":  7.15, "population":  355000},
    {"city": "Bielefeld",   "lat": 52.02, "lng":  8.53, "population":  340000},
    {"city": "Bonn",        "lat": 50.73, "lng":  7.10, "population":  330000},
    {"city": "Münster",     "lat": 51.96, "lng":  7.63, "population":  315000},
]


def load_from_csv(country_name: str) -> list[dict]:
    """Load city data for a country from worldcities.csv."""
    import os, csv
    csv_path = "worldcities.csv"
    if not os.path.exists(csv_path):
        print(f"❌  '{csv_path}' not found. Using built-in Germany dataset.")
        return []

    cities = []
    for enc in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            with open(csv_path, encoding=enc, newline="") as f:
                reader = csv.DictReader(f)
                # Normalise headers
                reader.fieldnames = [h.strip().lower() for h in reader.fieldnames]
                for row in reader:
                    if row.get("country","").strip().lower() != country_name.lower():
                        continue
                    try:
                        lat = float(row["lat"])
                        lng = float(row["lng"])
                    except (ValueError, KeyError):
                        continue
                    try:
                        pop = int(float(row.get("population") or 0))
                    except ValueError:
                        pop = 0
                    cities.append({
                        "city":       row.get("city","").strip(),
                        "lat":        lat,
                        "lng":        lng,
                        "population": pop,
                        "capital":    row.get("capital","").strip().lower(),
                    })
            break
        except UnicodeDecodeError:
            continue

    if not cities:
        # Try to find partial matches for a helpful error
        suggestions = set()
        try:
            with open(csv_path, encoding="utf-8-sig", newline="") as f:
                for row in csv.DictReader(f):
                    c = row.get("country","").strip()
                    if country_name.lower() in c.lower():
                        suggestions.add(c)
        except Exception:
            pass
        print(f"❌  No cities found for '{country_name}'.")
        if suggestions:
            print("    Did you mean:", ", ".join(sorted(suggestions)[:5]))
    else:
        print(f"    Loaded {len(cities)} cities for '{country_name}' from {csv_path}")
    return cities


# ── Prompt 14: Batch pre-generation for GitHub Pages ─────────────────────────
COUNTRIES_TO_PREGENERATE = [
    "Germany", "France", "Japan", "India", "China",
    "United States", "Brazil", "Thailand", "Australia",
    "United Kingdom", "Italy", "Spain", "Canada", "Mexico",
    "South Korea", "Indonesia", "Pakistan", "Nigeria",
    "Egypt", "Argentina", "Russia", "Turkey", "Iran",
    "Vietnam", "Philippines", "Ethiopia", "Tanzania",
    "Kenya", "Colombia", "Poland",
]


def batch_generate(countries: list = None) -> None:
    """Pre-generates gravity + concentration JSON for each country into data/<Country>/"""
    import os
    if countries is None:
        countries = COUNTRIES_TO_PREGENERATE

    narrator = InsightNarrator()
    ok, fail = 0, 0

    for country in countries:
        folder = os.path.join("data", country.replace(" ", "_"))
        os.makedirs(folder, exist_ok=True)

        try:
            cities = load_from_csv(country)
            if not cities:
                raise ValueError("No cities found in worldcities.csv")

            pairs  = calculate_gravity_pairs(cities)
            if not pairs:
                raise ValueError("Not enough cities with population data")

            report = calculate_concentration(cities, country)

            # Fold narration directly into report (no separate read-modify-write)
            narrative        = narrator.narrate_combined(report, pairs, cities)
            report["narration"] = narrative

            export_for_d3(cities, pairs, country,
                          path=os.path.join(folder, "gravity_data.json"))
            export_concentration(report,
                          path=os.path.join(folder, "concentration.json"))

            print(f"  OK  {country}")
            ok += 1
        except Exception as e:
            print(f"  FAIL  {country}: {e}")
            fail += 1

    print(f"\nBatch complete: {ok} OK, {fail} failed")
    if ok > 0:
        print("Commit the data/ folder to GitHub to enable static deployment.")


# ── Entry point ───────────────────────────────────────────────────────────────
cli_country = sys.argv[1] if len(sys.argv) > 1 else None

# Special arg: python generate_gravity.py --batch
if cli_country == "--batch":
    print("Pre-generating data for 30 countries -> data/ folder\n")
    batch_generate()
    sys.exit(0)

# Special arg: python generate_gravity.py global
if cli_country and cli_country.lower() == "global":
    print("Computing global urban primacy ranking from worldcities.csv…\n")
    compute_global_ranking()
    sys.exit(0)

if cli_country:
    print(f"Loading '{cli_country}' from worldcities.csv…")
    cities_data = load_from_csv(cli_country)
    if not cities_data:
        sys.exit(1)
    country_label = cli_country
else:
    cities_data   = germany
    country_label = "Germany"
    print("Using built-in Germany dataset (run 'python generate_gravity.py Japan' for other countries)")

print()

# gravity_data.json
pairs = calculate_gravity_pairs(cities_data)
if not pairs:
    print("No enough cities with population data to compute gravity pairs.")
    sys.exit(1)
export_for_d3(cities_data, pairs, country_label)

# concentration.json + narration
report    = calculate_concentration(cities_data, country_label)
narrator  = InsightNarrator()
narrative = narrator.narrate_combined(report, pairs, cities_data)
report["narration"] = narrative
export_concentration(report)
export_insight(narrative)   # appends narration into concentration.json (idempotent)

print(f"\nDone. Open http://localhost:8000")


# ── Prompt 10 self-test (runs when no CLI arg given) ──────────────────────────
def _run_self_tests():
    """Test narration with Germany (built-in), France, and Thailand from CSV."""
    narrator = InsightNarrator()
    separator = "─" * 60

    # ── Test 1: Germany (built-in) ──────────────────────────────────
    de_pairs  = calculate_gravity_pairs(germany)
    de_report = calculate_concentration(germany, "Germany")
    de_result = narrator.narrate_combined(de_report, de_pairs, germany)

    print(f"\n{'═'*60}")
    print("  TEST 1 — GERMANY  (polycentric / federal)")
    print(f"{'═'*60}")
    print(f"  Primacy Index : {de_report['primacy_index']} "
          f"({de_report['largest_city']['city']} @ {de_report['largest_city']['share_pct']}%)")
    print(f"  Pattern       : {de_result['concentration']['pattern']}")
    print(f"  Network       : {de_result['gravity']['network_type']}  "
          f"(avg top-5 dist: {de_result['gravity']['avg_distance_top5']} km)")
    print(f"  Headline      : {de_result['concentration']['headline']}")
    print(f"\n  SYNTHESIS:\n  {de_result['synthesis']}\n")

    # ── Test 2: France (CSV) ─────────────────────────────────────────
    fr_cities = load_from_csv("France")
    if fr_cities:
        fr_pairs  = calculate_gravity_pairs(fr_cities)
        fr_report = calculate_concentration(fr_cities, "France")
        fr_result = narrator.narrate_combined(fr_report, fr_pairs, fr_cities)

        print(separator)
        print("  TEST 2 — FRANCE  (dominant capital)")
        print(separator)
        print(f"  Primacy Index : {fr_report['primacy_index']} "
              f"({fr_report['largest_city']['city']} @ {fr_report['largest_city']['share_pct']}%)")
        print(f"  Pattern       : {fr_result['concentration']['pattern']}")
        print(f"  Network       : {fr_result['gravity']['network_type']}  "
              f"(avg top-5 dist: {fr_result['gravity']['avg_distance_top5']} km)")
        print(f"  Headline      : {fr_result['concentration']['headline']}")
        print(f"\n  SYNTHESIS:\n  {fr_result['synthesis']}\n")
    else:
        print(f"\n  TEST 2 — FRANCE: worldcities.csv not found, skipping.\n")

    # ── Test 3: Thailand (CSV) — high primacy ────────────────────────
    th_cities = load_from_csv("Thailand")
    if th_cities:
        th_pairs  = calculate_gravity_pairs(th_cities)
        th_report = calculate_concentration(th_cities, "Thailand")
        th_result = narrator.narrate_combined(th_report, th_pairs, th_cities)

        print(separator)
        print("  TEST 3 — THAILAND  (primate city dominance)")
        print(separator)
        print(f"  Primacy Index : {th_report['primacy_index']} "
              f"({th_report['largest_city']['city']} @ {th_report['largest_city']['share_pct']}%)")
        print(f"  Pattern       : {th_result['concentration']['pattern']}")
        print(f"  Network       : {th_result['gravity']['network_type']}  "
              f"(avg top-5 dist: {th_result['gravity']['avg_distance_top5']} km)")
        print(f"  Headline      : {th_result['concentration']['headline']}")
        print(f"\n  SYNTHESIS:\n  {th_result['synthesis']}\n")
    else:
        print(f"\n  TEST 3 — THAILAND: worldcities.csv not found, skipping.\n")


# Only run self-tests when using built-in dataset (no CLI arg)
if not cli_country:
    _run_self_tests()

import pandas as pd
import folium
import branca.colormap as cm
import os
import sys
import math

# ─────────────────────────────────────────────
# STEP 1: Check CSV exists
# ─────────────────────────────────────────────
CSV_PATH = "worldcities.csv"

if not os.path.exists(CSV_PATH):
    print("[ERROR] 'worldcities.csv' not found.")
    print("→ Download it manually from: https://simplemaps.com/data/world-cities")
    print("→ Unzip and place 'worldcities.csv' in the same folder as this script.")
    sys.exit(1)

# ─────────────────────────────────────────────
# STEP 2: Load the dataset
# ─────────────────────────────────────────────
df = pd.read_csv(CSV_PATH, on_bad_lines='skip', low_memory=False)

# ─────────────────────────────────────────────
# STEP 3: Clean relevant columns
# ─────────────────────────────────────────────
df = df[['city', 'lat', 'lng', 'country', 'population', 'capital']].copy()
df['lat']        = pd.to_numeric(df['lat'],        errors='coerce')
df['lng']        = pd.to_numeric(df['lng'],        errors='coerce')
df['population'] = pd.to_numeric(df['population'], errors='coerce')
df.dropna(subset=['lat', 'lng'], inplace=True)

# ─────────────────────────────────────────────
# STEP 4: User input — country selection
# ─────────────────────────────────────────────
print("📍 Example countries: Germany, France, India, Brazil, Japan, China, USA")
country_input = input("\nEnter country name: ").strip()

# Case-insensitive exact match
mask     = df['country'].str.lower() == country_input.lower()
filtered = df[mask].copy()

if filtered.empty:
    # Try partial match and suggest
    partial = df[df['country'].str.lower().str.contains(country_input.lower(), na=False)]
    if not partial.empty:
        suggestions = partial['country'].unique()[:5]
        print(f"\n[NOT FOUND] Did you mean: {', '.join(suggestions)}?")
    else:
        print(f"\n[NOT FOUND] No country matching '{country_input}' found.")
    sys.exit(1)

print(f"\n✅ Found {len(filtered)} cities in {country_input}")

# ─────────────────────────────────────────────
# STEP 5: Population scaling for circle radius
# ─────────────────────────────────────────────
pop_values = filtered['population'].dropna()
pop_min    = pop_values.min() if not pop_values.empty else 0
pop_max    = pop_values.max() if not pop_values.empty else 1

def scale_radius(pop, min_r=4, max_r=30):
    if pd.isna(pop) or pop <= 0:
        return min_r
    if pop_max == pop_min:
        return min_r
    norm = (math.sqrt(pop) - math.sqrt(pop_min)) / \
           (math.sqrt(pop_max) - math.sqrt(pop_min) + 1e-9)
    return min_r + norm * (max_r - min_r)

# ─────────────────────────────────────────────
# STEP 6: Color map — green → yellow → orange → red
# ─────────────────────────────────────────────
colormap = cm.LinearColormap(
    colors=['green', 'yellow', 'orange', 'red'],
    vmin=pop_min,
    vmax=pop_max,
    caption=f"Population — {country_input}"
)

# ─────────────────────────────────────────────
# STEP 7: Build the map centered on the country
# ─────────────────────────────────────────────
center_lat = filtered['lat'].mean()
center_lng = filtered['lng'].mean()

world_map = folium.Map(
    location=[center_lat, center_lng],
    zoom_start=5,
    tiles='CartoDB positron'
)

colormap.add_to(world_map)

# ─────────────────────────────────────────────
# STEP 8: Plot each city as a CircleMarker
# ─────────────────────────────────────────────
for _, row in filtered.iterrows():
    pop     = row['population']
    pop_str = f"{int(pop):,}" if not pd.isna(pop) else "N/A"
    is_capital = str(row['capital']).lower() in ['primary', 'admin', 'minor']
    fill_color = colormap(pop if not pd.isna(pop) else pop_min)

    popup_html = f"""
    <b style='font-size:14px'>{row['city']}</b><br>
    🌍 Country: {row['country']}<br>
    👥 Population: {pop_str}<br>
    🏛️ Capital: {'Yes' if is_capital else 'No'}
    """

    folium.CircleMarker(
        location=[row['lat'], row['lng']],
        radius=scale_radius(pop),
        color='black' if is_capital else fill_color,
        fill=True,
        fill_color=fill_color,
        fill_opacity=0.75,
        weight=2 if is_capital else 0.5,
        popup=folium.Popup(popup_html, max_width=220),
        tooltip=row['city']
    ).add_to(world_map)

# ─────────────────────────────────────────────
# STEP 9: Save and auto-open in browser
# ─────────────────────────────────────────────
output_file = f"{country_input.replace(' ', '_')}_map.html"
world_map.save(output_file)

print(f"\n🗺️  Map saved → '{output_file}'")

# Auto-open in default browser on Windows
import webbrowser
webbrowser.open(os.path.abspath(output_file))
print("🌐 Opening map in your browser...\n")
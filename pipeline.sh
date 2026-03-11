#!/usr/bin/env bash
# pipeline.sh — Filter worldcities.csv by country and output cities.json
# Usage: bash pipeline.sh        (Git Bash on Windows, or any POSIX shell)

set -euo pipefail

INPUT="worldcities.csv"
OUTPUT="cities.json"

echo "================================================"
echo "  World Cities Data Pipeline (Bash)"
echo "================================================"
echo ""

# ── Pre-flight checks ────────────────────────────────
if ! command -v awk &>/dev/null; then
  echo "❌  awk not found. Install Git Bash or WSL."
  exit 1
fi

if [[ ! -f "$INPUT" ]]; then
  echo "❌  '$INPUT' not found in: $(pwd)"
  echo "    Download it from: https://simplemaps.com/data/world-cities"
  exit 1
fi

read -rp "Enter country name: " country
echo ""

if [[ -z "$country" ]]; then
  echo "❌  Country name cannot be empty."
  exit 1
fi

echo "Processing '$country'…"

# ── Two-pass awk ─────────────────────────────────────
# Pass 1: count matching rows (for empty-result detection before writing)
count=$(awk -v ctry="$country" '
BEGIN { FS=","; n=0 }
NR==1 { next }
{
  # Strip surrounding double-quotes
  for (i=1; i<=NF; i++) { gsub(/^[[:space:]]*"/, "", $i); gsub(/"[[:space:]]*$/, "", $i) }
  if (tolower($5) != tolower(ctry)) next
  if ($3=="" || $4=="") next
  n++
}
END { print n }
' "$INPUT")

if [[ "$count" -eq 0 ]]; then
  echo ""
  echo "⚠️   No exact match for '$country'."
  echo "    Partial matches in dataset:"
  awk -v ctry="$country" '
  BEGIN { FS=","; found=0 }
  NR==1 { next }
  {
    for (i=1; i<=NF; i++) { gsub(/^"/, "", $i); gsub(/"$/, "", $i) }
    if (index(tolower($5), tolower(ctry)) > 0) {
      if (!seen[$5]++) { print "      •", $5; found++ }
      if (found >= 10) exit
    }
  }
  END { if (!found) print "    (none — check spelling)" }
  ' "$INPUT"
  exit 1
fi

# Pass 2: build JSON
awk -v ctry="$country" '
BEGIN {
  FS=","
  n=0
  printf "["
}
NR==1 { next }
{
  for (i=1; i<=NF; i++) { gsub(/^[[:space:]]*"/, "", $i); gsub(/"[[:space:]]*$/, "", $i) }

  city    = $1
  lat     = $3
  lng     = $4
  col5    = $5
  pop     = $10
  capital = $9

  if (tolower(col5) != tolower(ctry)) next
  if (lat=="" || lng=="") next

  # Validate lat/lng are numeric
  if (lat+0 == 0 && lat != "0") next
  if (lng+0 == 0 && lng != "0") next

  # Default missing / non-numeric population to 0
  if (pop=="" || pop=="NULL" || pop+0 != pop+0) pop = 0
  if (pop < 0) pop = 0

  # JSON-escape city and capital strings
  gsub(/\\/, "\\\\", city);    gsub(/"/, "\\\"", city)
  gsub(/\\/, "\\\\", capital); gsub(/"/, "\\\"", capital)

  if (n > 0) printf ","
  printf "\n  {\"city\":\"%s\",\"lat\":%s,\"lng\":%s,\"population\":%d,\"capital\":\"%s\"}",
    city, lat, lng, int(pop), tolower(capital)
  n++
}
END { printf "\n]\n" }
' "$INPUT" > "$OUTPUT"

# ── Summary ───────────────────────────────────────────
echo ""
echo "✅  $count cities exported for '$country'"
echo "    Output file : $OUTPUT"
echo ""
echo "------------------------------------------------"
echo "  Next steps:"
echo "    python -m http.server 8080"
echo "    Then open: http://localhost:8080"
echo "------------------------------------------------"

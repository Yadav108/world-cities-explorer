#!/usr/bin/env bash
# pipeline.sh — Filter worldcities.csv by country and output cities.json

echo "========================================"
echo "  World Cities Data Pipeline (Bash)"
echo "========================================"
echo ""
read -p "Enter country name: " country

if [[ -z "$country" ]]; then
  echo "Error: Country name cannot be empty."
  exit 1
fi

INPUT="worldcities.csv"

if [[ ! -f "$INPUT" ]]; then
  echo "Error: $INPUT not found in current directory."
  exit 1
fi

echo ""
echo "Processing '$country'..."

# Use awk to parse CSV, match country (col 5), and build JSON array
result=$(awk -v country="$country" '
BEGIN {
  FS=","
  count=0
  printf "["
}
NR==1 { next }  # skip header
{
  # Strip surrounding double-quotes from each field
  for (i=1; i<=NF; i++) {
    gsub(/^"/, "", $i)
    gsub(/"$/, "", $i)
  }

  city     = $1
  lat      = $3
  lng      = $4
  ctry     = $5
  pop      = $10
  capital  = $9

  # Case-insensitive country match
  if (tolower(ctry) != tolower(country)) next

  # Skip rows with missing lat/lng
  if (lat == "" || lng == "") next

  # Default missing population to 0
  if (pop == "" || pop == "NULL") pop = 0

  # Escape double-quotes in city/capital for JSON safety
  gsub(/"/, "\\\"", city)
  gsub(/"/, "\\\"", capital)

  if (count > 0) printf ","
  printf "\n  {\"city\":\"%s\",\"lat\":%s,\"lng\":%s,\"population\":%s,\"capital\":\"%s\"}",
    city, lat, lng, pop, capital
  count++
}
END {
  printf "\n]\n"
  print count > "/dev/stderr"
}
' "$INPUT")

count=$(echo "$result" | awk 'BEGIN{FS=","} NR==1{next} /^\s*\{/{c++} END{print c}')

# Capture stderr (the count line from awk)
count=$(awk -v country="$country" '
BEGIN { FS=","; count=0 }
NR==1 { next }
{
  for (i=1; i<=NF; i++) { gsub(/^"/, "", $i); gsub(/"$/, "", $i) }
  if (tolower($5) != tolower(country)) next
  if ($3 == "" || $4 == "") next
  count++
}
END { print count }
' "$INPUT")

echo "$result" > cities.json

echo ""
if [[ "$count" -eq 0 ]]; then
  echo "⚠  No cities found for '$country'."
  echo "   Check spelling or try a partial name in pipeline.py"
  exit 1
fi

echo "✅ Found $count cities for '$country'"
echo "   Saved to cities.json"
echo ""
echo "----------------------------------------"
echo "  Next steps:"
echo "    python -m http.server 8080"
echo "    Then open: http://localhost:8080"
echo "----------------------------------------"

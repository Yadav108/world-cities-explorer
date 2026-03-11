import sys
import os

# Check 1: Pandas
try:
    import pandas
    print("✓ pandas:", pandas.__version__)
except ImportError:
    print("✗ pandas: NOT INSTALLED")

# Check 2: CSV
import csv
try:
    r = list(csv.reader(open('worldcities.csv', encoding='utf-8')))
    print(f"✓ CSV rows: {len(r)}")
    print(f"  Columns: {r[0]}")
except Exception as e:
    print(f"✗ CSV error: {e}")

# Check 3: Pipeline test
import subprocess
try:
    result = subprocess.run([sys.executable, 'pipeline.py'], input='Japan\n', capture_output=True, text=True, timeout=10)
    if result.returncode == 0:
        print("✓ pipeline.py executed successfully")
        for line in result.stdout.split('\n')[-5:]:
            if line.strip():
                print(f"  {line}")
    else:
        print(f"✗ pipeline.py failed:\n{result.stderr}")
except Exception as e:
    print(f"✗ pipeline.py error: {e}")

# Check 4: cities.json
import json
try:
    if os.path.exists('cities.json'):
        d = json.load(open('cities.json'))
        print(f"✓ cities.json: {len(d)} records")
        print(f"  First 3:")
        for i, city in enumerate(d[:3], 1):
            print(f"    {i}. {city['city']}, {city['country']}")
    else:
        print("✗ cities.json: NOT FOUND")
except Exception as e:
    print(f"✗ cities.json error: {e}")

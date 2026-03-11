#!/usr/bin/env python3
"""
Verification script to check all dependencies and pipeline
"""

import csv
import json
import subprocess
import os
import sys

os.chdir(r"C:\Users\Aryan\PycharmProjects\pythonProject\100 day challenge")

print("=" * 60)
print("VERIFICATION CHECKS")
print("=" * 60)
print()

# Check 1: Pandas installation
print("✓ CHECK 1: Pandas Installation")
print("-" * 60)
try:
    import pandas
    print(f"✅ PASS: pandas {pandas.__version__} is installed")
except ImportError as e:
    print(f"❌ FAIL: pandas is not installed. Error: {e}")
    print("   Installing pandas...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas", "-q"])
    import pandas
    print(f"✅ pandas {pandas.__version__} installed successfully")

print()

# Check 2: CSV columns
print("✓ CHECK 2: worldcities.csv Columns")
print("-" * 60)
try:
    with open('worldcities.csv', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
        print(f"✅ PASS: CSV loaded successfully")
        print(f"   Total rows: {len(rows)}")
        print(f"   Columns: {rows[0]}")
except Exception as e:
    print(f"❌ FAIL: Could not read CSV. Error: {e}")

print()

# Check 3: Test pipeline with "Japan"
print("✓ CHECK 3: Test pipeline.py with 'Japan'")
print("-" * 60)
try:
    result = subprocess.run(
        [sys.executable, 'pipeline.py'],
        input='Japan\n',
        capture_output=True,
        text=True,
        timeout=10
    )
    if result.returncode == 0:
        print(f"✅ PASS: Pipeline executed successfully")
        print(f"   Output:\n{result.stdout}")
    else:
        print(f"❌ FAIL: Pipeline failed with error")
        print(f"   Error: {result.stderr}")
except Exception as e:
    print(f"❌ FAIL: Could not run pipeline. Error: {e}")

print()

# Check 4: Verify cities.json
print("✓ CHECK 4: Verify cities.json Was Created")
print("-" * 60)
try:
    if not os.path.exists('cities.json'):
        print(f"❌ FAIL: cities.json not found")
    else:
        with open('cities.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✅ PASS: cities.json exists and is valid JSON")
        print(f"   Total records: {len(data)}")
        if data:
            print(f"   First 3 records:")
            for i, record in enumerate(data[:3], 1):
                print(f"      {i}. {record['city']}, {record['country']} ({record['population']} pop)")
except Exception as e:
    print(f"❌ FAIL: Could not verify cities.json. Error: {e}")

print()
print("=" * 60)
print("VERIFICATION COMPLETE")
print("=" * 60)

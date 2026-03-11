#!/usr/bin/env python3
import os
import sys

# Change to the target directory
os.chdir(r'C:\Users\Aryan\PycharmProjects\pythonProject\100 day challenge')

files_to_delete = [
    '_write_index.py',
    'run_write.py',
    'final_write.py',
    'check_size.py',
    'delete_temp_files.py'
]

deleted = []
not_found = []
errors = []

print("Starting file deletion...")
print("-" * 50)

for filename in files_to_delete:
    try:
        if os.path.exists(filename):
            os.remove(filename)
            deleted.append(filename)
            print(f"✓ Deleted: {filename}")
        else:
            not_found.append(filename)
            print(f"✗ Not found: {filename}")
    except Exception as e:
        errors.append((filename, str(e)))
        print(f"✗ Error: {filename} - {str(e)}")

print("-" * 50)
print(f"\nResults:")
print(f"  Deleted: {len(deleted)}")
print(f"  Not found: {len(not_found)}")
print(f"  Errors: {len(errors)}")

if deleted:
    print(f"\nFiles deleted:")
    for f in deleted:
        print(f"  - {f}")

if not_found:
    print(f"\nFiles not found:")
    for f in not_found:
        print(f"  - {f}")

# Try to delete this script and previous helper script
for cleanup_file in ['execute_delete.py', 'delete_files.py']:
    try:
        if os.path.exists(cleanup_file):
            os.remove(cleanup_file)
            print(f"\n✓ Cleanup: Deleted {cleanup_file}")
    except:
        pass

import os

files_to_delete = [
    '_write_index.py',
    'run_write.py',
    'final_write.py',
    'check_size.py',
    'delete_temp_files.py'
]

deleted = []
not_found = []

for file in files_to_delete:
    try:
        os.remove(file)
        deleted.append(file)
        print(f'Deleted: {file}')
    except FileNotFoundError:
        not_found.append(file)
        print(f'Not found: {file}')
    except Exception as e:
        print(f'Error deleting {file}: {str(e)}')

print()
print(f'Summary: {len(deleted)} file(s) deleted, {len(not_found)} file(s) not found')

# Clean up this script too
os.remove('delete_files.py')
print('Cleanup: Deleted delete_files.py')

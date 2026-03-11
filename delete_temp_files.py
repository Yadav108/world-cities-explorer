import os

files = [
    r'C:\Users\Aryan\PycharmProjects\pythonProject\100 day challenge\_write_index.py',
    r'C:\Users\Aryan\PycharmProjects\pythonProject\100 day challenge\run_write.py',
    r'C:\Users\Aryan\PycharmProjects\pythonProject\100 day challenge\final_write.py',
    r'C:\Users\Aryan\PycharmProjects\pythonProject\100 day challenge\check_size.py'
]

for file_path in files:
    try:
        os.remove(file_path)
        print(f'Deleted: {file_path}')
    except FileNotFoundError:
        print(f'File not found: {file_path}')
    except Exception as e:
        print(f'Error deleting {file_path}: {e}')

# Clean up this script itself
script_path = r'C:\Users\Aryan\PycharmProjects\pythonProject\100 day challenge\delete_temp_files.py'
try:
    os.remove(script_path)
    print(f'Deleted: {script_path}')
except:
    pass

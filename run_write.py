import subprocess
import os

# Execute the write_index.py script
script_path = r'C:\Users\Aryan\PycharmProjects\pythonProject\100 day challenge\_write_index.py'
try:
    result = subprocess.run(['python', script_path], capture_output=True, text=True, timeout=30)
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)
    print("Return code:", result.returncode)
    
    # Check if file exists and get size
    html_file = r'C:\Users\Aryan\PycharmProjects\pythonProject\100 day challenge\index.html'
    if os.path.exists(html_file):
        size = os.path.getsize(html_file)
        print(f"✓ File created successfully, size: {size} bytes")
        
        # Read first 5 lines
        with open(html_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()[:5]
            print("First 5 lines:")
            for i, line in enumerate(lines, 1):
                print(f"{i}. {line.rstrip()}")
        
        # Read last 5 lines
        with open(html_file, 'r', encoding='utf-8') as f:
            all_lines = f.readlines()
            lines = all_lines[-5:]
            print("Last 5 lines:")
            for i, line in enumerate(lines, 1):
                print(f"{len(all_lines)-5+i}. {line.rstrip()}")
    else:
        print("✗ File was not created")
except Exception as e:
    print(f"Error: {e}")

import os
import json

def get_files(dir_path):
    files = []
    for root, _, filenames in os.walk(dir_path):
        for filename in filenames:
            if filename in ['.DS_Store']:
                continue
            filepath = os.path.join(root, filename)
            rel_path = os.path.relpath(filepath, 'c:\\Users\\H 4\\Downloads\\pos')
            rel_path = rel_path.replace('\\', '/')
            files.append(rel_path)
    return files

all_files = []
for f in os.listdir('c:\\Users\\H 4\\Downloads\\pos'):
    if f in ['node_modules', '.git', 'dist', '.kilo', '.local', '.vscode', '.netlify']:
        continue
    f_path = os.path.join('c:\\Users\\H 4\\Downloads\\pos', f)
    if os.path.isdir(f_path):
        all_files.extend(get_files(f_path))
    else:
        all_files.append(f)

total_size = 0
for f in all_files:
    total_size += os.path.getsize(os.path.join('c:\\Users\\H 4\\Downloads\\pos', f))

print(f"Total files: {len(all_files)}")
print(f"Total size: {total_size} bytes")

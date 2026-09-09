import re

file_path = r'd:\dbmss\app.py'

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

main_idx = -1
for i, line in enumerate(lines):
    if "if __name__ == '__main__':" in line:
        main_idx = i
        break

if main_idx != -1 and main_idx < len(lines) - 5:
    # Main block is not at the end! Let's move it to the very end.
    main_block = lines[main_idx:]
    rest_of_file = lines[:main_idx]
    
    new_lines = rest_of_file + ["\n"] + main_block
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print("Moved main block to the end successfully.")
else:
    print("Main block is already at the end.")

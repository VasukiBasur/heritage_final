import os

file_path = r'd:\dbmss\app.py'

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

main_idx = -1
for i, line in enumerate(lines):
    if "if __name__ == '__main__':" in line:
        main_idx = i
        break

if main_idx != -1:
    # Extract the 2 lines of the main block
    main_block = lines[main_idx:main_idx+2]
    
    # Remove those 2 lines from the rest of the file
    rest_of_file = lines[:main_idx] + lines[main_idx+2:]
    
    # Append them to the very end
    new_lines = rest_of_file + ["\n"] + main_block
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print("Main block moved to absolute end successfully.")
else:
    print("Main block not found.")

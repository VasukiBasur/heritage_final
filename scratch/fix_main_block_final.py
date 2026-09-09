import os

file_path = r'd:\dbmss\app.py'

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Filter out all lines that contain the main block components
new_lines = []
for line in lines:
    if "if __name__ == '__main__':" in line or "app.run(debug=True)" in line:
        continue
    new_lines.append(line)

# Append them safely at the end
new_lines.append("\nif __name__ == '__main__':\n")
new_lines.append("    app.run(debug=True)\n")

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print("Main block completely fixed and appended to end.")

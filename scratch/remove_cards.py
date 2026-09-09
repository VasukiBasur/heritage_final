with open('templates/supplier_tracking.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

start_idx = -1
end_idx = -1

for i, line in enumerate(lines):
    if '<div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3' in line:
        start_idx = i
        break

for i in range(len(lines)-1, -1, -1):
    if '<script>' in lines[i]:
        end_idx = i - 1
        break

if start_idx != -1 and end_idx != -1:
    new_lines = lines[:start_idx] + lines[end_idx:]
    with open('templates/supplier_tracking.html', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print('Successfully removed the transit cards grid.')
else:
    print('Could not find start or end index')

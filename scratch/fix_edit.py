import re

with open('templates/supplier_schedule.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace any edit button that doesn't have the onclick handler
pattern = re.compile(r'<button class="text-\[#d4af37\]/40 hover:text-\[#d4af37\] transition-colors" title="Edit">')
replacement = r'<button onclick="openEditModal(event, this)" class="text-[#d4af37]/40 hover:text-[#d4af37] transition-colors" title="Edit">'

text = pattern.sub(replacement, text)

with open('templates/supplier_schedule.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Fixed edit buttons successfully.')

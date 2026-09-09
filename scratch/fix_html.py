import re

with open('templates/supplier_schedule.html', 'r', encoding='utf-8') as f:
    text = f.read()

broken_pattern = re.compile(
    r'(<button class="text-\[#d4af37\]/40.*?</button>)\s*</div>\s*<div class="flex items-center">(<span class="w-2 h-2.*?></span>)</div>\s*</div>'
)

fixed_replacement = r'<div class="flex items-center space-x-2">\1\2</div>\n                </div>'

text = broken_pattern.sub(fixed_replacement, text)

# There is also one in the `confirmSchedule` JS block!
# Let's fix that too.
text = text.replace(
"""            <div class="flex justify-between items-start mb-2">
                <span class="text-[9px] text-green-400 uppercase tracking-widest font-bold">${timeStr}</span>
                <div class="flex items-center space-x-2">
                    <button class="text-[#d4af37]/40 hover:text-[#d4af37] transition-colors" title="Edit">    <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path></svg></button>
                    <span class="w-2 h-2 rounded-full bg-green-500"></span>
                </div>
            </div>""",
"""            <div class="flex justify-between items-center mb-2">
                <span class="text-[9px] text-green-400 uppercase tracking-widest font-bold">${timeStr}</span>
                <div class="flex items-center space-x-2">
                    <button class="text-[#d4af37]/40 hover:text-[#d4af37] transition-colors" title="Edit"><svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path></svg></button>
                    <span class="w-2 h-2 rounded-full bg-green-500"></span>
                </div>
            </div>""")

with open('templates/supplier_schedule.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Fixed HTML structure successfully.')

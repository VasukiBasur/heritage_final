import re

with open('templates/supplier_pickup.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Pattern to find the double wrapped block:
# <div class="flex items-center">\s*<div class="w-8 h-8 rounded-full[^>]+>[A-Z]{2}</div>\s*<div>\s*<div class="flex items-center">
# we will just replace the start of this block with just the inner <div class="flex items-center">
# AND we need to remove the trailing </div>\n</div>\n</div> that was generated.

# Wait, let's just do a brute force cleanup.
names = [
    ("Lakshmi Devi", "ID: ART-912", "LD", "bg-[#8b4513]", "text-white"),
    ("Syed Khaleel", "ID: ART-334", "SK", "bg-[#1a1a1a]", "text-[#d4af37]"),
    ("Parvati Patil", "ID: ART-501", "PP", "bg-[#333]", "text-white"),
    ("Vijay Jha", "ID: ART-909", "VJ", "bg-[#5a0000]", "text-white"),
    ("Ananya Acharya", "ID: ART-112", "AA", "bg-[#141414]", "text-[#d4af37]")
]

for name, id_str, initials, bg, text_col in names:
    # Notice the inner one has the wrong color because my script hardcoded it.
    # We just want to replace the WHOLE <td> content with the correct one.
    
    # We can use regex to find the td content for this person
    pattern = re.compile(r'(<td class="py-5 px-4">\s*<div class="flex items-center">.*?<p class="font-serif text-\[#f5ebd7\] font-semibold">' + name + r'</p>.*?</div>\s*</div>\s*</div>\s*</td>)', re.DOTALL)
    
    good_content = f'''<td class="py-5 px-4">
                        <div class="flex items-center">
                            <div class="w-8 h-8 rounded-full {bg} {text_col} flex items-center justify-center font-bold text-xs mr-3 border border-[#d4af37]/30">{initials}</div>
                            <div>
                                <p class="font-serif text-[#f5ebd7] font-semibold">{name}</p>
                                <p class="text-[10px] text-[#f5ebd7]/50 mt-0.5 uppercase tracking-widest">{id_str}</p>
                            </div>
                        </div>
                    </td>'''
                    
    text = pattern.sub(good_content, text)

with open('templates/supplier_pickup.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Duplicates fixed.")

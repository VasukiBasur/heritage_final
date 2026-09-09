import re

with open('templates/supplier_pickup.html', 'r', encoding='utf-8') as f:
    content = f.read()

def replace_td(match):
    name = match.group(1)
    id_text = match.group(2)
    
    # get initials
    parts = name.split()
    if len(parts) > 1:
        initials = (parts[0][0] + parts[1][0]).upper()
    else:
        initials = name[:2].upper()
        
    color_pool = ['bg-[#800000]', 'bg-[#8b4513]', 'bg-[#1a1a1a]', 'bg-[#333]', 'bg-[#5a0000]', 'bg-[#141414]']
    # simple hash for color
    color = color_pool[len(name) % len(color_pool)]
    
    # if it's the dark ones, text is gold, else white
    text_color = "text-[#d4af37]" if color in ['bg-[#1a1a1a]', 'bg-[#141414]'] else "text-white"
    
    return f'''<div class="flex items-center">
                            <div class="w-8 h-8 rounded-full {color} {text_color} flex items-center justify-center font-bold text-xs mr-3 border border-[#d4af37]/30">{initials}</div>
                            <div>
                                <p class="font-serif text-[#f5ebd7] font-semibold">{name}</p>
                                <p class="text-[10px] text-[#f5ebd7]/50 mt-0.5 uppercase tracking-widest">{id_text}</p>
                            </div>
                        </div>'''

# The pattern looks for:
# <p class="font-serif text-[#f5ebd7] font-semibold">Name</p>
# <p class="text-[10px] text-[#f5ebd7]/50 mt-0.5 uppercase tracking-widest">ID: ART-XXX</p>
# But only if it's NOT already wrapped in the flex items-center div.

# Let's just find and replace the two paragraphs inside the td
pattern = re.compile(r'<p class="font-serif text-\[#f5ebd7\] font-semibold">([^<]+)</p>\s*<p class="text-\[10px\] text-\[#f5ebd7\]/50 mt-0\.5 uppercase tracking-widest">([^<]+)</p>')

new_content = pattern.sub(replace_td, content)

with open('templates/supplier_pickup.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Done")

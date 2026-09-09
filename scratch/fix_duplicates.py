import re

with open('templates/supplier_pickup.html', 'r', encoding='utf-8') as f:
    content = f.read()

# The pattern to find the duplicate wrappers:
# We look for a <div class="flex items-center"> that contains another <div class="flex items-center"> exactly identical inside it.
# Actually, since it only happened to the 6 items in the Pending tab, we can just replace the outer wrapper with the inner one.

# Pattern: 
# <div class="flex items-center">\s*<div class="w-8 h-8 rounded-full .*?</div>\s*<div>\s*<div class="flex items-center">
# we just want to remove the first 3 lines and the last 2 lines of the outer wrapper.

pattern = re.compile(
    r'<div class="flex items-center">\s*<div class="w-8 h-8 rounded-full [^>]+>[A-Z]{2}</div>\s*<div>\s*(<div class="flex items-center">.*?</div>\s*</div>\s*</div>)',
    re.DOTALL
)

def remove_outer(match):
    # match.group(1) is the inner <div class="flex items-center">... down to its closing tags
    return match.group(1)

new_content = pattern.sub(remove_outer, content)

# But wait, the closing tags are also doubled:
# </div>\n                            </div>\n                        </div>
# My pattern captures the inner one, but we might leave trailing </div>s.
# Let's just do a simpler string replacement.

# Let's write a simple state machine or regex to find:
# <div class="flex items-center">
#   <div class="w-8 h-8...
#   <div>
#     <div class="flex items-center">
# and replace with just the inner <div class="flex items-center">

import re
with open('templates/supplier_pickup.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Find all blocks of:
# <div class="flex items-center">
#   <div class="...">XX</div>
#   <div>
#       <div class="flex items-center">
#       ...
#       </div>
#   </div>
# </div>

# Let's just use regex to strip out the outer layer.
# The outer layer is exactly:
# <div class="flex items-center">\s*<div class="w-8 h-8[^>]+>[A-Z]{2}</div>\s*<div>\s*
# and the closing is:
# \s*</div>\s*</div>

# Let's just do this:
# For each artisan name (Ramesh Kumar, Lakshmi Devi, Syed Khaleel, Parvati Patil, Vijay Jha, Ananya Acharya):
names = [
    ("Ramesh Kumar", "ID: ART-204", "RK", "bg-[#800000]", "text-white"),
    ("Lakshmi Devi", "ID: ART-912", "LD", "bg-[#8b4513]", "text-white"),
    ("Syed Khaleel", "ID: ART-334", "SK", "bg-[#1a1a1a]", "text-[#d4af37]"),
    ("Parvati Patil", "ID: ART-501", "PP", "bg-[#333]", "text-white"),
    ("Vijay Jha", "ID: ART-909", "VJ", "bg-[#5a0000]", "text-white"),
    ("Ananya Acharya", "ID: ART-112", "AA", "bg-[#141414]", "text-[#d4af37]")
]

for name, id_str, initials, bg, text_col in names:
    bad_block = f'''<div class="flex items-center">
                            <div class="w-8 h-8 rounded-full {bg} {text_col} flex items-center justify-center font-bold text-xs mr-3 border border-[#d4af37]/30">{initials}</div>
                            <div>
                                <div class="flex items-center">
                            <div class="w-8 h-8 rounded-full {bg} {text_col} flex items-center justify-center font-bold text-xs mr-3 border border-[#d4af37]/30">{initials}</div>
                            <div>
                                <p class="font-serif text-[#f5ebd7] font-semibold">{name}</p>
                                <p class="text-[10px] text-[#f5ebd7]/50 mt-0.5 uppercase tracking-widest">{id_str}</p>
                            </div>
                        </div>
                            </div>
                        </div>'''
                        
    good_block = f'''<div class="flex items-center">
                            <div class="w-8 h-8 rounded-full {bg} {text_col} flex items-center justify-center font-bold text-xs mr-3 border border-[#d4af37]/30">{initials}</div>
                            <div>
                                <p class="font-serif text-[#f5ebd7] font-semibold">{name}</p>
                                <p class="text-[10px] text-[#f5ebd7]/50 mt-0.5 uppercase tracking-widest">{id_str}</p>
                            </div>
                        </div>'''
    
    text = text.replace(bad_block, good_block)

with open('templates/supplier_pickup.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Duplicates removed.")

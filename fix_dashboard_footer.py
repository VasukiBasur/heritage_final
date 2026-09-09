import os
import re

app_file = r"d:\dbmss\templates\dashboard.html"

with open(app_file, 'r', encoding='utf-8') as f:
    content = f.read()

# We need to find the footer block and the closing tag of the main wrapper.
# The main wrapper closes right before the footer in the current file.
# The structure is:
# </main>
# </div>
# <!-- Footer -->
# <footer> ... </footer>

# Let's replace the order
pattern = r'(</main>\s*</div>)\s*(<!-- Footer -->\s*<footer class="bg-brand-black border-t border-brand-gold/20 py-8 mt-auto">.*?</footer>)'
replacement = r'\2\n\1'

new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open(app_file, 'w', encoding='utf-8') as f:
    f.write(new_content)
    
print("Dashboard footer fixed")

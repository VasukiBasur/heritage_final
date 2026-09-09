import os
import re
import glob

template_dir = r"d:\dbmss\templates"
all_html_files = glob.glob(os.path.join(template_dir, "*.html"))

pattern = r'(</main>\s*</div>)\s*(<!-- Footer -->\s*<footer class="bg-brand-black border-t border-brand-gold/20 py-8 mt-auto">.*?</footer>)'
replacement = r'\2\n\1'

for f in all_html_files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    if "<!-- Footer -->" in content and "</main>" in content:
        # Check if footer is outside the wrapper
        if re.search(pattern, content, flags=re.DOTALL):
            new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
            with open(f, 'w', encoding='utf-8') as file:
                file.write(new_content)
            print(f"Fixed footer in {os.path.basename(f)}")

import os
import re

template_dir = r"d:\dbmss\templates"

for root, dirs, files in os.walk(template_dir):
    for f in files:
        if f.endswith('.html'):
            filepath = os.path.join(root, f)
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Revert the max-w-[1600px] mx-auto and force full screen
            old_str1 = '<div class="px-4 py-6 md:px-6 lg:px-8 w-full max-w-[1600px] mx-auto" style="width: 100%;">'
            new_str1 = '<div class="w-full h-full px-8 lg:px-12">'
            
            old_str2 = '<div class="px-4 py-6 md:px-6 lg:px-8 w-full max-w-[1600px] mx-auto">'
            new_str2 = '<div class="w-full h-full px-8 lg:px-12">'
            
            # If not modified by previous script, replace original
            old_str3 = '<div class="px-4 py-6 md:px-6 lg:px-8 w-full" style="width: 100%;">'
            
            old_str4 = '<div class="px-4 py-6 md:px-6 lg:px-8 w-full">'
            
            if old_str1 in content:
                content = content.replace(old_str1, new_str1)
            elif old_str2 in content:
                content = content.replace(old_str2, new_str2)
            elif old_str3 in content:
                content = content.replace(old_str3, new_str1)
            elif old_str4 in content:
                content = content.replace(old_str4, new_str2)

            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"Forced full screen in {f}")

print("Full screen alignment applied.")

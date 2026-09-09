import os

template_dir = r"d:\dbmss\templates"

for root, dirs, files in os.walk(template_dir):
    for f in files:
        if f.endswith('.html'):
            filepath = os.path.join(root, f)
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # The pattern we want to fix in all main containers
            old_str1 = '<div class="px-4 py-6 md:px-6 lg:px-8 w-full" style="width: 100%;">'
            new_str1 = '<div class="px-4 py-6 md:px-6 lg:px-8 w-full max-w-[1600px] mx-auto" style="width: 100%;">'
            
            old_str2 = '<div class="px-4 py-6 md:px-6 lg:px-8 w-full">'
            new_str2 = '<div class="px-4 py-6 md:px-6 lg:px-8 w-full max-w-[1600px] mx-auto">'
            
            if old_str1 in content or old_str2 in content:
                new_content = content.replace(old_str1, new_str1).replace(old_str2, new_str2)
                with open(filepath, 'w', encoding='utf-8') as file:
                    file.write(new_content)
                print(f"Centered layout in {f}")

print("Alignment fix complete.")

import os

template_dir = r"d:\dbmss\templates"

for root, dirs, files in os.walk(template_dir):
    for f in files:
        if f.endswith('.html'):
            filepath = os.path.join(root, f)
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Step 1: Fix the master wrapper to be centered with max-width
            old_wrapper = '<!-- Main Content Wrapper -->\n    <div class="flex-1 flex flex-col h-full overflow-hidden">'
            new_wrapper = '<!-- Main Content Wrapper -->\n    <div class="flex-1 flex flex-col h-full overflow-hidden w-full max-w-[1500px] mx-auto relative shadow-[0_0_50px_rgba(0,0,0,0.8)]">'
            
            if old_wrapper in content:
                content = content.replace(old_wrapper, new_wrapper)
            
            # Step 2: Ensure inner content doesn't have weird padding or max-widths conflicting
            old_inner1 = '<div class="w-full h-full px-8 lg:px-12">'
            new_inner1 = '<div class="w-full h-full p-6 lg:p-10">'
            if old_inner1 in content:
                content = content.replace(old_inner1, new_inner1)

            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"Centered master layout in {f}")

print("Master alignment complete.")

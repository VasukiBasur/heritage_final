import os

templates = [
    r'd:\dbmss\templates\artisan_dashboard.html',
    r'd:\dbmss\templates\supplier_dashboard.html',
    r'd:\dbmss\templates\shipment_dashboard.html'
]

for file_path in templates:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix the Main Content Wrapper
    old_wrapper = '<div class="flex flex-col h-full overflow-hidden w-full relative">'
    new_wrapper = '<div class="flex-1 flex flex-col h-full overflow-hidden relative">'
    content = content.replace(old_wrapper, new_wrapper)
    
    # Move the footer inside the main block if it's currently outside
    # The footer looks like: <footer ...>...</footer>
    # We want to move it to just before </main>
    footer_start = content.find('<footer')
    footer_end = content.find('</footer>', footer_start) + 9
    
    main_end = content.find('</main>')
    
    if footer_start != -1 and main_end != -1 and footer_start > main_end:
        # Footer is outside main!
        footer_html = content[footer_start:footer_end]
        
        # Remove old footer
        content = content[:footer_start] + content[footer_end:]
        
        # Insert footer before </main>
        main_end = content.find('</main>')
        content = content[:main_end] + "\n    " + footer_html + "\n" + content[main_end:]
        
        # Now remove any extra empty lines left by old footer removal
        content = content.replace('\n\n\n', '\n\n')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed layout in {os.path.basename(file_path)}")

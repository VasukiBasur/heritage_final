import os

templates = {
    r'd:\dbmss\templates\dashboard.html': 'Admin Dashboard',
    r'd:\dbmss\templates\artisan_dashboard.html': 'Weaver Overview',
    r'd:\dbmss\templates\supplier_dashboard.html': 'Supplier Portal',
    r'd:\dbmss\templates\shipment_dashboard.html': 'Logistics Command'
}

for file_path, title in templates.items():
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the start of the actual content
    # For dashboard.html, it's after the flash messages block, or just inside <main>
    # Let's extract everything inside <main ...> and before <footer> or <script> or chatbot
    
    main_start = content.find('<main')
    if main_start != -1:
        # Find the end of the opening main tag
        main_content_start = content.find('>', main_start) + 1
        
        # Find where main ends
        main_end = content.rfind('</main>')
        
        if main_end != -1:
            main_content = content[main_content_start:main_end]
            
            # Remove any Flash Message blocks since base_layout.html already handles them!
            # We'll just remove {% with messages = get_flashed_messages ... {% endwith %}
            flash_start = main_content.find('{% with messages = get_flashed_messages')
            flash_end = main_content.find('{% endwith %}')
            if flash_start != -1 and flash_end != -1:
                main_content = main_content[:flash_start] + main_content[flash_end+13:]
            
            # Extract Chatbot and Scripts
            extra_scripts = ""
            chatbot_start = content.find('<!-- Advanced Floating AI Chatbot -->')
            if chatbot_start != -1:
                # The chatbot usually extends to the end of the file before </body>
                body_end = content.find('</body>')
                extra_scripts = content[chatbot_start:body_end]
                
                # if chatbot was inside main_content, remove it from main_content
                cb_in_main = main_content.find('<!-- Advanced Floating AI Chatbot -->')
                if cb_in_main != -1:
                    main_content = main_content[:cb_in_main]

            # Construct new file content
            new_content = f"{{% extends 'base_layout.html' %}}\n\n"
            new_content += f"{{% block title %}}{title}{{% endblock %}}\n"
            new_content += f"{{% block header_title %}}{title}{{% endblock %}}\n\n"
            new_content += f"{{% block content %}}\n"
            new_content += main_content
            new_content += f"\n{{% endblock %}}\n\n"
            
            if extra_scripts.strip():
                new_content += f"{{% block extra_scripts %}}\n"
                new_content += extra_scripts
                new_content += f"\n{{% endblock %}}\n"
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Migrated {os.path.basename(file_path)} successfully.")
        else:
            print(f"Could not find </main> in {os.path.basename(file_path)}")
    else:
        print(f"Could not find <main in {os.path.basename(file_path)}")

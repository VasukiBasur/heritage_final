import os
import glob

# The script migrates all *_module.html files to use the base_layout.html
template_dir = r'd:\dbmss\templates'
module_files = glob.glob(os.path.join(template_dir, '*_module.html'))

# Add specific files that aren't *module.html but need the sidebar
extra_files = [
    os.path.join(template_dir, 'demand_prediction.html'),
]
module_files.extend(extra_files)

def to_title_case(filename):
    name = os.path.basename(filename).replace('_module.html', '').replace('.html', '')
    return name.replace('_', ' ').title()

for file_path in module_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if already migrated
    if "{% extends 'base_layout.html' %}" in content:
        continue

    title = to_title_case(file_path)

    # 1. We need to extract the core content. Most of these modules have a <div class="glass-card"> that contains the main dashboard or table.
    # Alternatively, we can just extract everything between <body> and </body>, but we need to strip out any <nav> or sidebar or old header.
    
    # In the older templates, they usually had a <nav> for the topbar, or a sidebar.
    # Let's find where the real content starts. Usually it's after the top navbar.
    # Many of these files have a structure like:
    # <body class="flex h-screen ...">
    #   <aside>...</aside> (maybe)
    #   <div class="flex-1 ...">
    #      <header>...</header>
    #      <main ...> THIS IS WHAT WE WANT </main>
    
    main_start = content.find('<main')
    if main_start != -1:
        main_content_start = content.find('>', main_start) + 1
        main_end = content.rfind('</main>')
        
        if main_end != -1:
            main_content = content[main_content_start:main_end]
            
            # Remove any Flash Message blocks since base_layout.html already handles them!
            flash_start = main_content.find('{% with messages = get_flashed_messages')
            flash_end = main_content.find('{% endwith %}')
            if flash_start != -1 and flash_end != -1:
                main_content = main_content[:flash_start] + main_content[flash_end+13:]
            
            # Extract Scripts from the bottom (before </body>)
            extra_scripts = ""
            script_start = content.find('<script>', main_end)
            if script_start != -1:
                body_end = content.find('</body>')
                if body_end != -1:
                    extra_scripts = content[script_start:body_end]

            # Construct new file content
            new_content = f"{{% extends 'base_layout.html' %}}\n\n"
            new_content += f"{{% block title %}}{title}{{% endblock %}}\n"
            new_content += f"{{% block header_title %}}{title} Management{{% endblock %}}\n\n"
            new_content += f"{{% block content %}}\n"
            new_content += main_content
            new_content += f"\n{{% endblock %}}\n\n"
            
            if extra_scripts.strip():
                new_content += f"{{% block extra_scripts %}}\n"
                new_content += extra_scripts
                new_content += f"\n{{% endblock %}}\n"
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Migrated {os.path.basename(file_path)} successfully via <main> tag.")
            continue

    # If <main> is not found, fallback: Extract body, remove <nav>, <header>, <aside>
    body_start = content.find('<body')
    if body_start != -1:
        body_content_start = content.find('>', body_start) + 1
        body_end = content.find('</body>')
        if body_end != -1:
            body_content = content[body_content_start:body_end]
            
            # Strip <nav>
            nav_s = body_content.find('<nav')
            nav_e = body_content.find('</nav>')
            if nav_s != -1 and nav_e != -1:
                body_content = body_content[:nav_s] + body_content[nav_e+6:]
            
            # Strip <header>
            hdr_s = body_content.find('<header')
            hdr_e = body_content.find('</header>')
            if hdr_s != -1 and hdr_e != -1:
                body_content = body_content[:hdr_s] + body_content[hdr_e+9:]
                
            # Strip <aside>
            aside_s = body_content.find('<aside')
            aside_e = body_content.find('</aside>')
            if aside_s != -1 and aside_e != -1:
                body_content = body_content[:aside_s] + body_content[aside_e+8:]
            
            # Strip Flash
            flash_s = body_content.find('{% with messages = get_flashed_messages')
            flash_e = body_content.find('{% endwith %}')
            if flash_s != -1 and flash_e != -1:
                body_content = body_content[:flash_s] + body_content[flash_e+13:]
            
            # Find scripts
            scripts = ""
            script_s = body_content.find('<script')
            if script_s != -1:
                scripts = body_content[script_s:]
                body_content = body_content[:script_s]

            # Construct new
            new_content = f"{{% extends 'base_layout.html' %}}\n\n"
            new_content += f"{{% block title %}}{title}{{% endblock %}}\n"
            new_content += f"{{% block header_title %}}{title} Management{{% endblock %}}\n\n"
            new_content += f"{{% block content %}}\n"
            new_content += body_content
            new_content += f"\n{{% endblock %}}\n\n"
            
            if scripts.strip():
                new_content += f"{{% block extra_scripts %}}\n"
                new_content += scripts
                new_content += f"\n{{% endblock %}}\n"
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Migrated {os.path.basename(file_path)} successfully via <body> fallback.")

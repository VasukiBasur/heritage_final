import re

# 1. Update artisans.html
with open('d:\\dbmss\\templates\\artisans.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_header = '<h3 class="text-2xl font-serif font-semibold text-brand-gold mb-2">{{ artisan.name }}</h3>'
new_header = '<h3 class="text-2xl font-serif font-semibold text-brand-gold mb-2">{{ artisan.name }} <span class="text-[10px] text-brand-lightgold/50 align-top ml-2 font-mono bg-brand-gold/10 px-1.5 py-0.5 rounded border border-brand-gold/20 tracking-wider">#ART-{{ artisan.artisan_id }}</span></h3>'

html = html.replace(old_header, new_header)

with open('d:\\dbmss\\templates\\artisans.html', 'w', encoding='utf-8') as f:
    f.write(html)


# 2. Update app.py queries to add ORDER BY a.name ASC
with open('d:\\dbmss\\app.py', 'r', encoding='utf-8') as f:
    app_py = f.read()

old_artisans_query = """        LEFT JOIN production_logs p ON a.artisan_id = p.artisan_id
        GROUP BY a.artisan_id
    \"\"\")"""

new_artisans_query = """        LEFT JOIN production_logs p ON a.artisan_id = p.artisan_id
        GROUP BY a.artisan_id
        ORDER BY a.name ASC
    \"\"\")"""

app_py = app_py.replace(old_artisans_query, new_artisans_query)

old_weaver_query = 'cursor.execute("SELECT artisan_id, name, village, skill_level, contact_number, experience_years, wage_details FROM artisans")'
new_weaver_query = 'cursor.execute("SELECT artisan_id, name, village, skill_level, contact_number, experience_years, wage_details FROM artisans ORDER BY name ASC")'

app_py = app_py.replace(old_weaver_query, new_weaver_query)

with open('d:\\dbmss\\app.py', 'w', encoding='utf-8') as f:
    f.write(app_py)

print("Artisans ordered alphabetically and ID shown.")

import re
import os

# 1. Update app.py
app_path = r"d:\dbmss\app.py"
with open(app_path, 'r', encoding='utf-8') as f:
    app_content = f.read()

# Add get form variables for village, experience, wage
app_content = re.sub(
    r'skill\s*=\s*request\.form\[\'skill_level\'\]',
    "skill = request.form['skill_level']\n        village = request.form.get('village', 'Harapanahalli')\n        experience_years = request.form.get('experience_years', 10)\n        wage_details = request.form.get('wage_details', '₹800/day')",
    app_content
)

# Update SQL statement WITH image
app_content = re.sub(
    r'UPDATE artisans\s+SET name=%s, location=%s, contact_number=%s, skill_level=%s, image_file=%s\s+WHERE artisan_id=%s\s+""", \(name, location, contact, skill, image_file, id\)',
    'UPDATE artisans \n                    SET name=%s, location=%s, contact_number=%s, skill_level=%s, image_file=%s, village=%s, experience_years=%s, wage_details=%s \n                    WHERE artisan_id=%s\n                """, (name, location, contact, skill, image_file, village, experience_years, wage_details, id)',
    app_content
)

# Update SQL statement WITHOUT image
app_content = re.sub(
    r'UPDATE artisans\s+SET name=%s, location=%s, contact_number=%s, skill_level=%s\s+WHERE artisan_id=%s\s+""", \(name, location, contact, skill, id\)',
    'UPDATE artisans \n                    SET name=%s, location=%s, contact_number=%s, skill_level=%s, village=%s, experience_years=%s, wage_details=%s \n                    WHERE artisan_id=%s\n                """, (name, location, contact, skill, village, experience_years, wage_details, id)',
    app_content
)

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(app_content)
print("Updated app.py")


# 2. Update edit_artisan.html
edit_path = r"d:\dbmss\templates\edit_artisan.html"
with open(edit_path, 'r', encoding='utf-8') as f:
    edit_content = f.read()

new_fields = """
                <div>
                    <label for="village" class="block text-sm font-medium text-brand-lightgold/70 uppercase tracking-widest mb-2">Village</label>
                    <input type="text" id="village" name="village" value="{{ artisan.village }}" required class="w-full px-4 py-3 rounded-sm transition-all">
                </div>
                <div>
                    <label for="experience_years" class="block text-sm font-medium text-brand-lightgold/70 uppercase tracking-widest mb-2">Experience (Years)</label>
                    <input type="number" id="experience_years" name="experience_years" value="{{ artisan.experience_years }}" required class="w-full px-4 py-3 rounded-sm transition-all">
                </div>
                <div>
                    <label for="wage_details" class="block text-sm font-medium text-brand-lightgold/70 uppercase tracking-widest mb-2">Wage Details</label>
                    <input type="text" id="wage_details" name="wage_details" value="{{ artisan.wage_details }}" required class="w-full px-4 py-3 rounded-sm transition-all">
                </div>
"""

edit_content = re.sub(
    r'(<div>\s*<label for="skill_level".*?</label>\s*<input type="text" id="skill_level" name="skill_level".*?</div>)',
    r'\1\n' + new_fields,
    edit_content,
    flags=re.DOTALL
)

with open(edit_path, 'w', encoding='utf-8') as f:
    f.write(edit_content)
print("Updated edit_artisan.html")


# 3. Update artisans.html display cards
artisans_path = r"d:\dbmss\templates\artisans.html"
with open(artisans_path, 'r', encoding='utf-8') as f:
    artisans_content = f.read()

new_display = """<p class="flex justify-between border-b border-brand-gold/10 pb-2 group-hover:border-brand-gold/30 transition-colors"><span class="font-semibold text-brand-gold/70 group-hover:text-brand-gold transition-colors">Contact</span> <span>{{ artisan.contact_number }}</span></p>
                            <p class="flex justify-between border-b border-brand-gold/10 pb-2 group-hover:border-brand-gold/30 transition-colors"><span class="font-semibold text-brand-gold/70 group-hover:text-brand-gold transition-colors">Experience</span> <span>{{ artisan.experience_years }} Years</span></p>
                            <p class="flex justify-between border-b border-brand-gold/10 pb-2 group-hover:border-brand-gold/30 transition-colors"><span class="font-semibold text-brand-gold/70 group-hover:text-brand-gold transition-colors">Wage</span> <span>{{ artisan.wage_details }}</span></p>"""

artisans_content = re.sub(
    r'<p class="flex justify-between border-b border-brand-gold/10 pb-2 group-hover:border-brand-gold/30 transition-colors"><span class="font-semibold text-brand-gold/70 group-hover:text-brand-gold transition-colors">Contact</span> <span>\{\{ artisan\.contact_number \}\}</span></p>',
    new_display,
    artisans_content
)

with open(artisans_path, 'w', encoding='utf-8') as f:
    f.write(artisans_content)
print("Updated artisans.html")

print("Execution complete.")

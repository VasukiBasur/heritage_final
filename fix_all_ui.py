import os
import re
import mysql.connector
from dotenv import load_dotenv
import glob

# 1. Update Database for Eri Silk Image
load_dotenv()
try:
    db = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )
    cursor = db.cursor()
    cursor.execute("UPDATE raw_materials SET image_file='eri_silk.png.jpeg' WHERE material_name LIKE '%Eri Silk%'")
    db.commit()
    cursor.close()
    db.close()
    print("Database updated for Eri Silk.")
except Exception as e:
    print(f"DB Error: {e}")

# 2. Fix PolarArea Chart Axes in Dashboard
app_file = r"d:\dbmss\templates\dashboard.html"
with open(app_file, 'r', encoding='utf-8') as f:
    content = f.read()

# We need to remove the scales block from options for productionChart
# The script currently has:
# scales: { y: { ... }, x: { ... } }
# Let's replace the scales block with nothing
pattern = r"scales:\s*\{\s*y:\s*\{[^}]+\},\s*x:\s*\{[^}]+\}\s*\}"
content = re.sub(pattern, "scales: { r: { grid: { color: 'rgba(212, 175, 55, 0.1)' }, ticks: { display: false } } }", content)

with open(app_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("Dashboard chart fixed.")


# 3. Universal Search Script Injection
template_dir = r"d:\dbmss\templates"
all_html_files = glob.glob(os.path.join(template_dir, "*.html"))

universal_search = """
    <!-- Universal Search Script -->
    <script>
        document.addEventListener("DOMContentLoaded", function() {
            const searchInputs = document.querySelectorAll('input[type="text"][placeholder*="Search"]');
            searchInputs.forEach(searchInput => {
                searchInput.addEventListener("input", function(e) {
                    const query = e.target.value.toLowerCase();
                    
                    // Filter Table Rows
                    const tables = document.querySelectorAll("table tbody");
                    tables.forEach(tbody => {
                        const rows = tbody.querySelectorAll("tr");
                        rows.forEach(row => {
                            if (row.innerText.toLowerCase().includes(query)) {
                                row.style.display = "";
                            } else {
                                row.style.display = "none";
                            }
                        });
                    });

                    // Filter Glass Cards (for Modules like Designs/Materials)
                    const cards = document.querySelectorAll(".glass-card");
                    cards.forEach(card => {
                        // Avoid filtering structural glass cards (like dashboard charts)
                        if (card.parentElement && card.parentElement.tagName === 'BODY') return;
                        if (card.querySelector('canvas')) return; // ignore charts
                        
                        // Only filter if it's likely a grid card
                        if (card.innerText.toLowerCase().includes(query)) {
                            if(card.parentElement && card.parentElement.style) card.parentElement.style.display = "block";
                            card.style.display = "block";
                        } else {
                            if(card.parentElement && card.parentElement.style && card.parentElement.tagName !== 'DIV') card.parentElement.style.display = "none";
                            card.style.display = "none";
                        }
                    });
                });
            });
        });
    </script>
</body>
"""

for f in all_html_files:
    if "artisans.html" in f: continue # artisans.html already has a specialized search script
    with open(f, 'r', encoding='utf-8') as file:
        file_content = file.read()
    
    if "Universal Search Script" not in file_content:
        file_content = file_content.replace("</body>", universal_search)
        with open(f, 'w', encoding='utf-8') as file:
            file.write(file_content)

print("Universal search injected.")

import re

app_file = r"d:\dbmss\templates\dashboard.html"

with open(app_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix Artisan Chart Binding
content = content.replace("item.total_logs", "item.count")

# Make Artisan Chart "Advanced" (Gradient & glowing borders)
old_artisan_bg = "backgroundColor: 'rgba(34, 197, 94, 0.7)',"
new_artisan_bg = """backgroundColor: [
                                    'rgba(212, 175, 55, 0.8)',
                                    'rgba(230, 200, 90, 0.6)',
                                    'rgba(180, 150, 40, 0.6)',
                                    'rgba(255, 220, 110, 0.6)',
                                    'rgba(150, 120, 30, 0.6)'
                                ],
                                borderColor: 'rgba(212, 175, 55, 1)',
                                borderWidth: 2,"""
content = content.replace(old_artisan_bg, new_artisan_bg)
# Remove the old borderColor/borderWidth/borderRadius right after it, if we injected it in the block above
content = re.sub(r"borderColor: '#22c55e',\s*borderWidth: 1,\s*borderRadius: 4", "borderRadius: 4", content)


# Fix Status Chart Route
content = content.replace("fetch('/api/stats/status_distribution')", "fetch('/api/stats/order_status')")

# Fix Status Chart Binding (assuming it's mapping item.count)
# Let's ensure it has the right bindings. The original has data.map(item => item.count) probably.
# Let's upgrade its look (add cutout and better colors)
old_status_type = "type: 'doughnut',"
new_status_type = "type: 'doughnut',"
# Actually, doughnut is fine, let's just make sure it renders beautifully.
# The user wants "advance level graph", so maybe we add some options.
old_status_options = """options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            plugins: {
                                legend: {
                                    position: 'right',
                                    labels: { color: '#f0e6d2', padding: 20, font: { family: "'Inter', sans-serif" } }
                                }
                            },
                            cutout: '75%',
                            borderWidth: 0
                        }"""
# Let's try replacing options just in case it doesn't have cutout
content = re.sub(r"options:\s*\{[^}]+legend:[^}]+labels:[^}]+}[^}]+}[^}]+}[^}]+}", old_status_options, content)

with open(app_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("Graphs fixed and advanced.")

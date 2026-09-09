import os
import re

app_file = r"d:\dbmss\app.py"
artisans_file = r"d:\dbmss\templates\artisans.html"
dashboard_file = r"d:\dbmss\templates\dashboard.html"

# --- 1. Fix artisans images (Passport style) ---
with open(artisans_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Change height to h-64 and object-center to object-top
content = content.replace('class="w-full bg-[#121212] relative group h-56"', 'class="w-full bg-[#121212] relative group h-72"')
content = content.replace('object-cover object-center', 'object-cover object-top')
# Fallback if they were already object-top
content = content.replace('h-56', 'h-72')

with open(artisans_file, 'w', encoding='utf-8') as f:
    f.write(content)


# --- 2. Inject missing /api/production_stats into app.py ---
with open(app_file, 'r', encoding='utf-8') as f:
    app_content = f.read()

stats_route = """@app.route('/api/production_stats')
@login_required
def production_stats():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
        
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT d.name, COUNT(p.log_id) as count
        FROM traditional_designs d
        LEFT JOIN production_logs p ON d.design_id = p.design_id
        GROUP BY d.design_id, d.name
    ''')
    stats = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(stats)
"""

if '/api/production_stats' not in app_content:
    # Inject it before the api_crud or api_chat route
    app_content = app_content.replace("@app.route('/api/chat'", stats_route + "\n@app.route('/api/chat'")
    with open(app_file, 'w', encoding='utf-8') as f:
        f.write(app_content)

# --- 3. Make Graph Advanced in dashboard.html ---
with open(dashboard_file, 'r', encoding='utf-8') as f:
    dash_content = f.read()

old_chart_js = """type: 'bar',
                        data: {
                            labels: labels,
                            datasets: [{
                                label: 'Production Volume',
                                data: counts,
                                backgroundColor: 'rgba(212, 175, 55, 0.7)',
                                borderColor: 'rgba(212, 175, 55, 1)',
                                borderWidth: 1,
                                borderRadius: 2
                            }]
                        },"""

advanced_chart_js = """type: 'polarArea',
                        data: {
                            labels: labels,
                            datasets: [{
                                label: 'Production Volume',
                                data: counts,
                                backgroundColor: [
                                    'rgba(212, 175, 55, 0.7)',
                                    'rgba(180, 50, 50, 0.7)',
                                    'rgba(50, 180, 50, 0.7)',
                                    'rgba(50, 50, 180, 0.7)',
                                    'rgba(212, 100, 55, 0.7)'
                                ],
                                borderColor: 'rgba(30, 30, 30, 1)',
                                borderWidth: 2
                            }]
                        },"""

if "type: 'bar'," in dash_content and "Production Volume Chart Script" in dash_content:
    dash_content = dash_content.replace(old_chart_js, advanced_chart_js)
    with open(dashboard_file, 'w', encoding='utf-8') as f:
        f.write(dash_content)

print("Fixes applied: artisans cropping, graph route restored, and graph upgraded.")

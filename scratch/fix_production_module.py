import re

with open('d:\\dbmss\\templates\\production_module.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix Add New button
html = html.replace(
    '<button class="bg-brand-gold text-brand-black px-4 py-2 rounded text-sm font-bold hover:bg-yellow-500 transition-colors">+ Add New</button>',
    '<a href="{{ url_for(\'add_log\') }}" class="bg-brand-gold text-brand-black px-4 py-2 rounded text-sm font-bold hover:bg-yellow-500 transition-colors inline-block">+ Add New</a>'
)

# Fix Select options and form for Save Stage
select_old = """
                <select class="bg-brand-dark border border-brand-gold/30 text-xs px-2 py-1 rounded text-brand-lightgold focus:outline-none focus:border-brand-gold">
                    <option value="Dyeing" {% if log.stage == 'Dyeing' %}selected{% endif %}>Dyeing</option>
                    <option value="Spinning" {% if log.stage == 'Spinning' %}selected{% endif %}>Spinning</option>
                    <option value="Weaving" {% if log.stage == 'Weaving' %}selected{% endif %}>Weaving</option>
                    <option value="Finishing" {% if log.stage == 'Finishing' %}selected{% endif %}>Finishing</option>
                    <option value="Packaging" {% if log.stage == 'Packaging' %}selected{% endif %}>Packaging</option>
                </select>
"""

select_new = """
                <form action="{{ url_for('update_stage', log_id=log.log_id) }}" method="POST" class="flex items-center space-x-2">
                    <select name="stage" class="bg-brand-dark border border-brand-gold/30 text-xs px-2 py-1 rounded text-brand-lightgold focus:outline-none focus:border-brand-gold">
                        <option value="Ordered" {% if log.stage == 'Ordered' %}selected{% endif %}>Ordered</option>
                        <option value="Raw_Material_Supply" {% if log.stage == 'Raw_Material_Supply' %}selected{% endif %}>Raw Material Supply</option>
                        <option value="Manufacturing" {% if log.stage == 'Manufacturing' %}selected{% endif %}>Manufacturing</option>
                        <option value="Distribution" {% if log.stage == 'Distribution' %}selected{% endif %}>Distribution</option>
                        <option value="Retail" {% if log.stage == 'Retail' %}selected{% endif %}>Retail</option>
                        <option value="Sold" {% if log.stage == 'Sold' %}selected{% endif %}>Sold</option>
                    </select>
"""

if select_old.strip() in html:
    html = html.replace(select_old, select_new)
else:
    # If indentation is slightly different
    html = re.sub(r'<select class="bg-brand-dark.*?</select>', select_new.strip(), html, flags=re.DOTALL)

button_old = '<td><button class="text-xs text-green-400 hover:underline">Save Stage</button></td>'
button_new = '<td><button type="submit" class="text-xs text-green-400 hover:underline px-2 py-1 border border-green-400/30 rounded bg-green-900/30">Save</button></form></td>'

if button_old in html:
    html = html.replace(button_old, button_new)
else:
    html = re.sub(r'<td><button class="text-xs text-green-400 hover:underline">Save Stage</button></td>', button_new, html)


# Also in app.py we should redirect add_log to production_module instead of admin_dashboard
with open('d:\\dbmss\\app.py', 'r', encoding='utf-8') as f:
    app_py = f.read()

app_py = app_py.replace(
    'flash("Production log added successfully!", "success")\n            return redirect(url_for(\'admin_dashboard\'))',
    'flash("Production log added successfully!", "success")\n            return redirect(url_for(\'production_module\'))'
)

app_py = app_py.replace(
    'return redirect(request.referrer or url_for(\'admin_dashboard\'))',
    'return redirect(request.referrer or url_for(\'production_module\'))'
)

with open('d:\\dbmss\\app.py', 'w', encoding='utf-8') as f:
    f.write(app_py)

with open('d:\\dbmss\\templates\\production_module.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Production tracking module fixed.")

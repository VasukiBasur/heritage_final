import os

filepath = r"d:\dbmss\templates\dashboard.html"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add "Stage" column header
content = content.replace('<th class="px-8 py-4 text-left text-xs font-semibold text-brand-gold uppercase tracking-wider">Status</th>',
                          '<th class="px-8 py-4 text-left text-xs font-semibold text-brand-gold uppercase tracking-wider">Status</th>\n                            <th class="px-8 py-4 text-left text-xs font-semibold text-brand-gold uppercase tracking-wider">Stage & QR</th>')

# 2. Add QR code and Dropdown column cell
# Need to find the Status cell and insert after it
old_status_cell = """                            <td class="px-8 py-5 whitespace-nowrap">
                                <span class="px-3 py-1 inline-flex text-xs leading-5 font-semibold rounded-full bg-brand-gold/10 text-brand-gold border border-brand-gold/20">
                                    {{ log.status }}
                                </span>
                            </td>"""

new_stage_cell = """                            <td class="px-8 py-5 whitespace-nowrap">
                                <span class="px-3 py-1 inline-flex text-xs leading-5 font-semibold rounded-full bg-brand-gold/10 text-brand-gold border border-brand-gold/20">
                                    {{ log.status }}
                                </span>
                            </td>
                            <td class="px-8 py-5 whitespace-nowrap flex items-center space-x-4">
                                <form action="{{ url_for('update_stage', log_id=log.log_id) }}" method="POST" class="flex items-center space-x-2">
                                    <select name="stage" class="bg-brand-black text-brand-lightgold border border-brand-gold/30 rounded-sm text-xs px-2 py-1 focus:outline-none focus:border-brand-gold">
                                        <option value="Ordered" {% if log.supply_chain_stage == 'Ordered' %}selected{% endif %}>Ordered</option>
                                        <option value="Raw_Material_Supply" {% if log.supply_chain_stage == 'Raw_Material_Supply' %}selected{% endif %}>Raw Material Supply</option>
                                        <option value="Manufacturing" {% if log.supply_chain_stage == 'Manufacturing' %}selected{% endif %}>Manufacturing</option>
                                        <option value="Distribution" {% if log.supply_chain_stage == 'Distribution' %}selected{% endif %}>Distribution</option>
                                        <option value="Retail" {% if log.supply_chain_stage == 'Retail' %}selected{% endif %}>Retail</option>
                                        <option value="Sold" {% if log.supply_chain_stage == 'Sold' %}selected{% endif %}>Sold</option>
                                    </select>
                                    <button type="submit" class="bg-brand-gold text-brand-black px-2 py-1 rounded-sm text-xs font-bold hover:bg-yellow-500">Update</button>
                                </form>
                                <img src="{{ url_for('generate_qr', log_id=log.log_id) }}" alt="QR Code" class="w-10 h-10 border border-brand-gold/50 rounded-sm hover:scale-150 transition-transform">
                            </td>"""

if old_status_cell in content:
    content = content.replace(old_status_cell, new_stage_cell)
else:
    print("Could not find status cell in dashboard.html. It might have different indentation.")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated dashboard.html with QR and Stage dropdown.")

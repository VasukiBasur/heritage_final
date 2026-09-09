import os
import glob
import re

template_dir = r"d:\dbmss\templates"

# 1. Replace form enctype and add file input in edit_artisan and edit_design
file_input = """
            <div class="mt-4">
                <label for="image" class="block text-xs font-semibold text-brand-lightgold/70 uppercase tracking-widest mb-2">Upload Image</label>
                <input type="file" name="image" id="image" accept="image/*" class="mt-4 block w-full text-sm text-gray-300 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-yellow-600 file:text-white hover:file:bg-yellow-700">
            </div>
"""

for fname in ['edit_artisan.html', 'edit_design.html']:
    filepath = os.path.join(template_dir, fname)
    if not os.path.exists(filepath): continue
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add enctype
    content = content.replace('<form method="POST"', '<form method="POST" enctype="multipart/form-data"')
    
    # Add file input before the submit button
    content = content.replace('<button type="submit"', file_input + '\n            <button type="submit"')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# 2. Update display images in grids to use the dynamic uploaded paths
# The user said: Update all display <img> tags in the grids to dynamically point to: {{ url_for('static', filename='uploads/' + item.image_file) }}

# artisans.html
filepath = os.path.join(template_dir, 'artisans.html')
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()
content = re.sub(r'src="\{\{ url_for\(\'static\', filename=\'images/weaver\.jpg\'\) \}\}"', 
                 r'src="{{ url_for(\'static\', filename=\'uploads/\' + artisan.image_file) }}"', content)
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

# designs.html and buyer_marketplace.html
for fname in ['designs.html', 'buyer_marketplace.html']:
    filepath = os.path.join(template_dir, fname)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    content = re.sub(r'src="\{\{ url_for\(\'static\', filename=\'images/saree\.jpg\'\) \}\}"', 
                     r'src="{{ url_for(\'static\', filename=\'uploads/\' + design.image_file) }}"', content)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# materials.html
filepath = os.path.join(template_dir, 'materials.html')
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()
content = re.sub(r'src="\{\{ url_for\(\'static\', filename=\'images/materials\.jpg\'\) \}\}"', 
                 r'src="{{ url_for(\'static\', filename=\'uploads/\' + material.image_file) }}"', content)
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

# 3. Update the chatbot JS in all templates
old_chat_js = """                    let text = msg.toLowerCase();
                    let reply = "Hello! I am your Handloom AI Assistant. How can I help you analyze the database today?";
                    if(text.includes('material')) reply = "We currently track 4 primary raw materials in the database, including Mulberry Silk and Gold Zari.";
                    else if(text.includes('artisan') || text.includes('weaver')) reply = "We have active artisans registered. Master weavers currently receive a 1.5x skill multiplier on their base payout.";
                    else if(text.includes('design') || text.includes('saree') || text.includes('top')) reply = "The Mysore Silk Zari is our most active production line this week, followed closely by the Ilkal Checkered pattern.";
                    
                    const aiDiv = document.createElement('div');
                    aiDiv.className = 'flex justify-start';
                    aiDiv.innerHTML = `<div class="bg-brand-black border border-brand-gold/20 rounded-lg rounded-tl-none px-3 py-2 max-w-[85%]">${reply}</div>`;
                    chatMessages.appendChild(aiDiv);
                    chatMessages.scrollTop = chatMessages.scrollHeight;
                }, 600);"""

new_chat_js = """                    let text = msg.toLowerCase();
                    
                    fetch('/api/chat', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({text: text}),
                    })
                    .then(response => response.json())
                    .then(data => {
                        const aiDiv = document.createElement('div');
                        aiDiv.className = 'flex justify-start';
                        aiDiv.innerHTML = `<div class="bg-brand-black border border-brand-gold/20 rounded-lg rounded-tl-none px-3 py-2 max-w-[85%]">${data.reply}</div>`;
                        chatMessages.appendChild(aiDiv);
                        chatMessages.scrollTop = chatMessages.scrollHeight;
                    })
                    .catch((error) => {
                        console.error('Error:', error);
                    });
                }, 600);"""

for filepath in glob.glob(os.path.join(template_dir, "*.html")):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    if old_chat_js in content:
        content = content.replace(old_chat_js, new_chat_js)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated chatbot JS in {filepath}")

import os
import glob

old_code = """                    let text = msg.toLowerCase();
                    let reply = "I am processing your request regarding the supply chain.";
                    if(text.includes('material')) reply = "We currently track 4 primary raw materials in the database, including Mulberry Silk and Gold Zari. Would you like to see the inventory levels?";
                    else if(text.includes('artisan') || text.includes('weaver')) reply = "We have 9 active artisans registered. Master weavers currently receive a 1.5x skill multiplier on their base payout.";
                    else if(text.includes('design') || text.includes('saree') || text.includes('top')) reply = "The Mysore Silk Zari is our most active production line this week, followed closely by the Ilkal Checkered pattern.";
                    else if(text.includes('hi') || text.includes('hello')) reply = "Hello! I am your Handloom AI Assistant. How can I help you analyze the database today?";
                    
                    const aiDiv = document.createElement('div');
                    aiDiv.className = 'flex justify-start';
                    aiDiv.innerHTML = `<div class="bg-brand-black border border-brand-gold/20 rounded-lg rounded-tl-none px-3 py-2 max-w-[85%]">${reply}</div>`;
                    chatMessages.appendChild(aiDiv);
                    chatMessages.scrollTop = chatMessages.scrollHeight;
                }, 400);"""

new_code = """                    let text = msg.toLowerCase();
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

template_dir = r"d:\dbmss\templates"
for filepath in glob.glob(os.path.join(template_dir, "*.html")):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    if old_code in content:
        content = content.replace(old_code, new_code)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated {filepath}")
    else:
        print(f"Skipped {filepath} - pattern not found")

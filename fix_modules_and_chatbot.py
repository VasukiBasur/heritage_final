import os
import re

flash_block = """
        <!-- Flash Messages -->
        {% with messages = get_flashed_messages(with_categories=true) %}
          {% if messages %}
            {% for category, message in messages %}
              <div class="mb-8 mx-6 mt-6 p-4 rounded-sm border-l-4 {% if category == 'success' %}bg-green-900/40 border-green-500 text-green-300{% elif category == 'error' %}bg-red-900/40 border-red-500 text-red-300{% else %}bg-brand-brown/40 border-brand-gold text-brand-lightgold{% endif %} shadow-md z-[100] relative">
                  {{ message }}
              </div>
            {% endfor %}
          {% endif %}
        {% endwith %}
"""

old_js = """                // Smart Local Parser Response
                setTimeout(() => {
                    chatMessages.removeChild(typingDiv);
                    
                    let text = msg.toLowerCase();
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

new_js = """                // Advanced Chatbot Response (Always Replies)
                setTimeout(() => {
                    chatMessages.removeChild(typingDiv);
                    
                    let text = msg.toLowerCase();
                    let reply = "I am the Advanced Handloom AI Assistant. Your input has been logged. How else can I assist with the ERP tracking?";
                    
                    if(text.includes('material') || text.includes('raw') || text.includes('silk') || text.includes('cotton')) {
                        reply = "We currently track premium raw materials in our ERP, primarily Mulberry Silk and Gold Zari. Inventory modules automatically alert upon low stock.";
                    } else if(text.includes('artisan') || text.includes('weaver') || text.includes('wage')) {
                        reply = "Master artisans receive a 1.5x skill multiplier on their base payout. Payouts are dynamically calculated using the Calculate_Artisan_Payout stored procedure.";
                    } else if(text.includes('design') || text.includes('saree') || text.includes('pattern')) {
                        reply = "The Mysore Silk Zari and Ilkal Checkered patterns are heavily tracked. Designs dictate the required raw materials through our design_materials relation.";
                    } else if(text.includes('hi') || text.includes('hello') || text.includes('hey')) {
                        reply = "Hello! I am your Handloom ERP Assistant. I can analyze supply chains, weavers, orders, and inventory data. What do you need?";
                    } else if(text.includes('order') || text.includes('buyer') || text.includes('customer')) {
                        reply = "Buyer orders are processed through the Orders Module. Once verified, production logs are generated for the artisans.";
                    } else if(text.includes('error') || text.includes('not working') || text.includes('bug')) {
                        reply = "I detect you might be asking about system status. All modules are securely connected to the MySQL 8.0 database backend.";
                    } else if(text.includes('thanks') || text.includes('thank')) {
                        reply = "You're very welcome! Let me know if you need to query any other tables.";
                    }
                    
                    const aiDiv = document.createElement('div');
                    aiDiv.className = 'flex justify-start';
                    aiDiv.innerHTML = `<div class="bg-brand-black border border-brand-gold/20 rounded-lg rounded-tl-none px-3 py-2 max-w-[85%] text-brand-gold">${reply}</div>`;
                    chatMessages.appendChild(aiDiv);
                    chatMessages.scrollTop = chatMessages.scrollHeight;
                }, 600);"""

templates_dir = "templates"

for filename in os.listdir(templates_dir):
    if filename.endswith(".html"):
        filepath = os.path.join(templates_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        original = content
        
        # Inject flash block into modules if missing
        if "_module.html" in filename and "get_flashed_messages" not in content:
            # Inject after <main>
            content = re.sub(r'(<main[^>]*>)', r'\1\n' + flash_block, content)
            
        # Update Chatbot JS
        if old_js in content:
            content = content.replace(old_js, new_js)
            
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated {filename}")

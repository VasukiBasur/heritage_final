import os
import re

saree_img = "https://images.unsplash.com/photo-1610030469983-98e550d615ef?q=80&w=400&auto=format&fit=crop"
artisan_img = "https://images.unsplash.com/photo-1580211516089-8b010fdfbf52?q=80&w=400&auto=format&fit=crop"
material_img = "https://images.unsplash.com/photo-1605289355680-75fb41239154?q=80&w=400&auto=format&fit=crop"

old_saree_regex = r"https://image\.pollinations\.ai/prompt/traditional-indian-handloom-silk-saree-gold-zari-dark-background-premium\?width=400&height=250&nologo=true"
old_artisan_regex = r"https://image\.pollinations\.ai/prompt/indian-artisan-weaving-at-wooden-handloom-warm-golden-hour-lighting\?width=400&height=250&nologo=true"
old_material_regex = r"https://image\.pollinations\.ai/prompt/spools-of-golden-silk-thread-and-cotton-yarn-cinematic-lighting-high-resolution\?width=400&height=250&nologo=true"

old_js = """                // Simulate AI response
                setTimeout(() => {
                    chatMessages.removeChild(typingDiv);
                    const aiDiv = document.createElement('div');
                    aiDiv.className = 'flex justify-start';
                    aiDiv.innerHTML = `<div class="bg-brand-black border border-brand-gold/20 rounded-lg rounded-tl-none px-3 py-2 max-w-[85%]">Hello! I am your Handloom AI Assistant. Our current top-selling design is the Mysore Silk Zari. How can I help you analyze the supply chain today?</div>`;
                    chatMessages.appendChild(aiDiv);
                    chatMessages.scrollTop = chatMessages.scrollHeight;
                }, 1000);"""

new_js = """                // Real AI response
                fetch('https://text.pollinations.ai/prompt/' + encodeURIComponent('Act as a handloom expert: ' + msg))
                    .then(response => response.text())
                    .then(text => {
                        chatMessages.removeChild(typingDiv);
                        const aiDiv = document.createElement('div');
                        aiDiv.className = 'flex justify-start';
                        aiDiv.innerHTML = `<div class="bg-brand-black border border-brand-gold/20 rounded-lg rounded-tl-none px-3 py-2 max-w-[85%]">${text}</div>`;
                        chatMessages.appendChild(aiDiv);
                        chatMessages.scrollTop = chatMessages.scrollHeight;
                    })
                    .catch(err => {
                        chatMessages.removeChild(typingDiv);
                        const aiDiv = document.createElement('div');
                        aiDiv.className = 'flex justify-start';
                        aiDiv.innerHTML = `<div class="bg-brand-black border border-brand-gold/20 rounded-lg rounded-tl-none px-3 py-2 max-w-[85%] text-red-400">Sorry, I'm offline right now.</div>`;
                        chatMessages.appendChild(aiDiv);
                        chatMessages.scrollTop = chatMessages.scrollHeight;
                    });"""

templates_dir = "templates"

def process_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    original = content
    
    # Replace images
    content = re.sub(old_saree_regex, saree_img, content)
    content = re.sub(old_artisan_regex, artisan_img, content)
    content = re.sub(old_material_regex, material_img, content)
    
    # Replace JS
    if old_js in content:
        content = content.replace(old_js, new_js)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filepath}")

for filename in os.listdir(templates_dir):
    if filename.endswith(".html"):
        process_html_file(os.path.join(templates_dir, filename))
        
print("All templates updated.")

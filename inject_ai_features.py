import os
import re

chat_widget_html = """
    <!-- Floating AI Chatbot -->
    <div id="ai-chat-widget" class="fixed bottom-6 right-6 z-50 font-sans">
        <button id="chat-toggle-btn" class="w-14 h-14 bg-brand-dark border-2 border-brand-gold rounded-full shadow-2xl flex items-center justify-center text-brand-gold hover:bg-brand-black transition-colors transform hover:scale-110">
            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M18 10c0 3.866-3.582 7-8 7a8.841 8.841 0 01-4.083-.98L2 17l1.338-3.123C2.493 12.767 2 11.434 2 10c0-3.866 3.582-7 8-7s8 3.134 8 7zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z" clip-rule="evenodd"></path></svg>
        </button>
        
        <div id="chat-window" class="hidden absolute bottom-16 right-0 w-80 h-96 bg-brand-dark border border-brand-gold rounded-lg shadow-2xl flex flex-col overflow-hidden">
            <div class="bg-brand-black border-b border-brand-gold/30 px-4 py-3 flex justify-between items-center">
                <div class="flex items-center space-x-2">
                    <div class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                    <h3 class="text-brand-gold font-serif font-bold text-sm">Handloom AI Assistant</h3>
                </div>
                <button id="chat-close-btn" class="text-brand-lightgold/50 hover:text-brand-gold transition-colors">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
                </button>
            </div>
            
            <div id="chat-messages" class="flex-grow p-4 overflow-y-auto space-y-3 bg-brand-dark/80 text-sm text-brand-lightgold">
                <div class="flex justify-start">
                    <div class="bg-brand-black border border-brand-gold/20 rounded-lg rounded-tl-none px-3 py-2 max-w-[85%]">
                        Welcome! How can I help you analyze the supply chain today?
                    </div>
                </div>
            </div>
            
            <div class="p-3 bg-brand-black border-t border-brand-gold/30">
                <form id="chat-form" class="flex items-center space-x-2">
                    <input type="text" id="chat-input" placeholder="Ask AI..." class="flex-grow bg-brand-dark text-brand-lightgold border border-brand-gold/30 rounded-sm px-3 py-2 focus:outline-none focus:border-brand-gold text-sm" autocomplete="off">
                    <button type="submit" class="bg-brand-gold text-brand-black hover:bg-yellow-500 px-3 py-2 rounded-sm transition-colors font-bold">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path></svg>
                    </button>
                </form>
            </div>
        </div>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            if (window.chatInitialized) return;
            window.chatInitialized = true;
            
            const chatWidget = document.getElementById('ai-chat-widget');
            if (!chatWidget) return;
            
            const toggleBtn = document.getElementById('chat-toggle-btn');
            const closeBtn = document.getElementById('chat-close-btn');
            const chatWindow = document.getElementById('chat-window');
            const chatForm = document.getElementById('chat-form');
            const chatInput = document.getElementById('chat-input');
            const chatMessages = document.getElementById('chat-messages');
            
            toggleBtn.addEventListener('click', () => {
                chatWindow.classList.toggle('hidden');
                if (!chatWindow.classList.contains('hidden')) {
                    chatInput.focus();
                }
            });
            
            closeBtn.addEventListener('click', () => {
                chatWindow.classList.add('hidden');
            });
            
            chatForm.addEventListener('submit', (e) => {
                e.preventDefault();
                const msg = chatInput.value.trim();
                if (!msg) return;
                
                // Add user message
                const userDiv = document.createElement('div');
                userDiv.className = 'flex justify-end';
                userDiv.innerHTML = `<div class="bg-brand-gold text-brand-black font-medium rounded-lg rounded-tr-none px-3 py-2 max-w-[85%]">${msg}</div>`;
                chatMessages.appendChild(userDiv);
                
                chatInput.value = '';
                chatMessages.scrollTop = chatMessages.scrollHeight;
                
                // Add typing indicator
                const typingDiv = document.createElement('div');
                typingDiv.className = 'flex justify-start typing-indicator';
                typingDiv.innerHTML = `<div class="bg-brand-black border border-brand-gold/20 rounded-lg rounded-tl-none px-3 py-2 flex space-x-1"><div class="w-1.5 h-1.5 bg-brand-gold/50 rounded-full animate-bounce"></div><div class="w-1.5 h-1.5 bg-brand-gold/50 rounded-full animate-bounce" style="animation-delay: 0.1s"></div><div class="w-1.5 h-1.5 bg-brand-gold/50 rounded-full animate-bounce" style="animation-delay: 0.2s"></div></div>`;
                chatMessages.appendChild(typingDiv);
                chatMessages.scrollTop = chatMessages.scrollHeight;
                
                // Simulate AI response
                setTimeout(() => {
                    chatMessages.removeChild(typingDiv);
                    const aiDiv = document.createElement('div');
                    aiDiv.className = 'flex justify-start';
                    aiDiv.innerHTML = `<div class="bg-brand-black border border-brand-gold/20 rounded-lg rounded-tl-none px-3 py-2 max-w-[85%]">Hello! I am your Handloom AI Assistant. Our current top-selling design is the Mysore Silk Zari. How can I help you analyze the supply chain today?</div>`;
                    chatMessages.appendChild(aiDiv);
                    chatMessages.scrollTop = chatMessages.scrollHeight;
                }, 1000);
            });
        });
    </script>
</body>"""

material_img = "https://image.pollinations.ai/prompt/spools-of-golden-silk-thread-and-cotton-yarn-cinematic-lighting-high-resolution?width=400&height=250&nologo=true"
saree_img = "https://image.pollinations.ai/prompt/traditional-indian-handloom-silk-saree-gold-zari-dark-background-premium?width=400&height=250&nologo=true"
artisan_img = "https://image.pollinations.ai/prompt/indian-artisan-weaving-at-wooden-handloom-warm-golden-hour-lighting?width=400&height=250&nologo=true"

templates_dir = "templates"

def process_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    original = content
    
    # 1. Swap image URLs
    # Dashboard hero images: url_for('static', filename='images/saree.png')
    content = re.sub(r"\{\{\s*url_for\('static',\s*filename='images/saree\.png'\)\s*\}\}", saree_img, content)
    content = re.sub(r"\{\{\s*url_for\('static',\s*filename='images/weaver\.png'\)\s*\}\}", artisan_img, content)
    content = re.sub(r"\{\{\s*url_for\('static',\s*filename='images/motif\.png'\)\s*\}\}", material_img, content)
    
    # Placeholder swaps
    # materials
    content = re.sub(r'<img src="https://via\.placeholder\.com/[^"]+" alt="[^"]*material[^"]*"', f'<img src="{material_img}" alt="Material"', content, flags=re.IGNORECASE)
    content = re.sub(r'<img src="https://via\.placeholder\.com/[^"]+" alt="\{\{ material\.material_name \}\}"', f'<img src="{material_img}" alt="{{{{ material.material_name }}}}"', content)
    
    # designs/sarees
    content = re.sub(r'<img src="https://via\.placeholder\.com/[^"]+" alt="Design Motif"', f'<img src="{saree_img}" alt="Design Motif"', content)
    content = re.sub(r'<img src="https://via\.placeholder\.com/[^"]+" alt="Saree"', f'<img src="{saree_img}" alt="Saree"', content)
    
    # artisans
    content = re.sub(r'<img src="https://via\.placeholder\.com/[^"]+" alt="Artisan"', f'<img src="{artisan_img}" alt="Artisan"', content)
    content = re.sub(r'<img src="https://via\.placeholder\.com/[^"]+" alt="Handloom Weaver"', f'<img src="{artisan_img}" alt="Handloom Weaver"', content)

    # 2. Inject chat widget before </body>
    if 'id="ai-chat-widget"' not in content:
        content = content.replace('</body>', chat_widget_html)
        
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filepath}")

for filename in os.listdir(templates_dir):
    if filename.endswith(".html"):
        process_html_file(os.path.join(templates_dir, filename))
        
print("\nSERVER READY: Click here -> http://127.0.0.1:5000")

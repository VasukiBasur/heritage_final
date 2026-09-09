import os

file_path = 'd:/dbmss/templates/shop_messages.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add IDs to chat input and messages container
content = content.replace('<div class="flex-1 p-6 overflow-y-auto space-y-4">', '<div id="chat-messages" class="flex-1 p-6 overflow-y-auto space-y-4">')
content = content.replace('placeholder="Type a message..." class="flex-1 bg-black', 'id="chat-input" placeholder="Type a message..." class="flex-1 bg-black')
content = content.replace('onclick="window.showToast(\'Message sent successfully!\')"', 'onclick="sendMessage()"')

# We need to replace the static chat bubbles with dynamic rendering, so we empty the chat messages div (except for the Today badge)
chat_html_to_replace = """<div class="flex justify-end">
                    <div class="bg-brand-gold text-black rounded-2xl rounded-tr-sm px-4 py-2 max-w-[70%]">
                        <p class="text-sm">Hi, can I get an update on my recent order?</p>
                        <span class="text-[10px] opacity-70 block text-right mt-1">10:24 AM</span>
                    </div>
                </div>

                <div class="flex justify-start">
                    <div class="bg-[#1a1a1a] border border-gray-800 text-gray-300 rounded-2xl rounded-tl-sm px-4 py-2 max-w-[70%]">
                        <p class="text-sm">Hello! Your order #ORD-8921 has been shipped and is currently in transit. You can track it in the Live Tracking section.</p>
                        <span class="text-[10px] text-gray-500 block mt-1">10:26 AM</span>
                    </div>
                </div>"""

content = content.replace(chat_html_to_replace, "")

js_script = """
    // Chat Management Logic
    const defaultMessages = [
        { sender: 'me', text: 'Hi, can I get an update on my recent order?', time: '10:24 AM' },
        { sender: 'support', text: 'Hello! Your order #ORD-8921 has been shipped and is currently in transit. You can track it in the Live Tracking section.', time: '10:26 AM' }
    ];

    function renderMessages() {
        let messages = JSON.parse(localStorage.getItem('userMessages'));
        if (!messages || messages.length === 0) {
            messages = defaultMessages;
            localStorage.setItem('userMessages', JSON.stringify(messages));
        }

        const container = document.getElementById('chat-messages');
        // Clear all but the 'Today' badge
        container.innerHTML = '<div class="flex flex-col items-center mb-6"><span class="text-xs text-gray-500 bg-[#111] px-3 py-1 rounded-full">Today</span></div>';

        messages.forEach(msg => {
            const div = document.createElement('div');
            if (msg.sender === 'me') {
                div.className = 'flex justify-end';
                div.innerHTML = `
                    <div class="bg-brand-gold text-black rounded-2xl rounded-tr-sm px-4 py-2 max-w-[70%]">
                        <p class="text-sm">${msg.text}</p>
                        <span class="text-[10px] opacity-70 block text-right mt-1">${msg.time}</span>
                    </div>`;
            } else {
                div.className = 'flex justify-start';
                div.innerHTML = `
                    <div class="bg-[#1a1a1a] border border-gray-800 text-gray-300 rounded-2xl rounded-tl-sm px-4 py-2 max-w-[70%]">
                        <p class="text-sm">${msg.text}</p>
                        <span class="text-[10px] text-gray-500 block mt-1">${msg.time}</span>
                    </div>`;
            }
            container.appendChild(div);
        });
        
        container.scrollTop = container.scrollHeight;
    }

    window.sendMessage = function() {
        const input = document.getElementById('chat-input');
        const text = input.value.trim();
        if (!text) return;

        let messages = JSON.parse(localStorage.getItem('userMessages')) || defaultMessages;
        const now = new Date();
        const timeStr = now.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        
        messages.push({ sender: 'me', text: text, time: timeStr });
        localStorage.setItem('userMessages', JSON.stringify(messages));
        
        input.value = '';
        renderMessages();
    };

    // Handle Enter key
    document.addEventListener("DOMContentLoaded", () => {
        renderMessages();
        document.getElementById('chat-input').addEventListener('keypress', function (e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    });
</script>
"""

content = content.replace('</script>', js_script)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Messages logic updated.")

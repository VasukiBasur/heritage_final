import os
import re

app_file = r"d:\dbmss\app.py"

with open(app_file, 'r', encoding='utf-8') as f:
    app_content = f.read()

# --- 1. Fix Production Stats ---
old_stats = """    cursor.execute(\"\"\"
        SELECT d.name, COUNT(p.log_id) as count
        FROM production_logs p
        JOIN traditional_designs d ON p.design_id = d.design_id
        GROUP BY d.design_id, d.name
    \"\"\")"""

new_stats = """    cursor.execute(\"\"\"
        SELECT d.name, COUNT(p.log_id) as count
        FROM traditional_designs d
        LEFT JOIN production_logs p ON d.design_id = p.design_id
        GROUP BY d.design_id, d.name
    \"\"\")"""

app_content = app_content.replace(old_stats, new_stats)

# --- 2. Fix Chatbot to use Pollinations AI ---
old_chat_pattern = r"@app\.route\('/api/chat', methods=\['POST'\]\).*?return jsonify\(\{\"reply\": reply\}\)"

new_chat = """import requests
import urllib.parse

@app.route('/api/chat', methods=['POST'])
def api_chat():
    data = request.get_json()
    text = data.get('text', '').strip()
    
    # System Context for the AI
    system_prompt = "You are an AI assistant for Heritage Handloom, an ERP system managing the textile supply chain (Artisans, Materials, Warehouses). Provide brief, helpful answers."
    
    try:
        # Use Pollinations AI for text generation (Free, no auth)
        encoded_prompt = urllib.parse.quote(f"{system_prompt}\\nUser: {text}")
        response = requests.get(f"https://text.pollinations.ai/{encoded_prompt}", timeout=10)
        
        if response.status_code == 200:
            reply = response.text.strip()
        else:
            reply = "I'm having trouble connecting to my neural network right now. Please try again later."
            
    except Exception as e:
        print(f"Chatbot API Error: {e}")
        # Fallback to hardcoded logic if the API fails or is blocked
        text_lower = text.lower()
        if 'hello' in text_lower or 'hi' in text_lower:
            reply = "Namaskara! I am your Handloom AI. How can I assist you today?"
        elif 'artisan' in text_lower or 'weaver' in text_lower:
            reply = "We have many master artisans in our network, primarily from Harapanahalli and Ilkal."
        else:
            reply = "I'm currently running in offline mode and can only answer basic queries about artisans and materials."
            
    return jsonify({"reply": reply})"""

app_content = re.sub(old_chat_pattern, new_chat, app_content, flags=re.DOTALL)

# Ensure requests is imported at the top if not already (it's in the new block now, but let's make sure it doesn't crash)
if "import requests" not in app_content[:500]:
    app_content = "import requests\n" + app_content

with open(app_file, 'w', encoding='utf-8') as f:
    f.write(app_content)

print("Applied fixes to production stats and chatbot API.")

import os
import re

print("Searching for saved credentials, emails, and passwords across the project...")

found = []
for root, dirs, files in os.walk('.'):
    if '.venv' in root or '__pycache__' in root or '.git' in root:
        continue
    for f in files:
        if f.endswith(('.py', '.sql', '.md', '.txt', '.html', '.env', '.json', '.js')):
            p = os.path.join(root, f)
            try:
                content = open(p, encoding='utf-8', errors='ignore').read()
                emails = set(re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', content))
                # filter out obvious domain dummy strings like text.pollinations.ai, socket.AF_INET etc
                valid_emails = {e for e in emails if not e.endswith(('.png', '.jpeg', '.jpg', '.webp', '.js', '.css')) and '@' in e}
                
                passwords = re.findall(r'(?:password|passwd|pwd)\s*[:=]\s*[\'"]([^\'"]+)[\'"]', content, re.IGNORECASE)
                hashes = re.findall(r'generate_password_hash\([\'"]([^\'"]+)[\'"]', content)
                user_inserts = re.findall(r'INSERT\s+INTO\s+users[^\;]+;', content, re.IGNORECASE)
                
                if valid_emails or passwords or hashes or user_inserts:
                    found.append({
                        'file': p,
                        'emails': list(valid_emails),
                        'passwords': passwords,
                        'hashes': hashes,
                        'user_inserts': user_inserts
                    })
            except Exception as e:
                pass

for item in found:
    print(f"\n--- {item['file']} ---")
    if item['emails']:
        print("  Emails:", item['emails'])
    if item['passwords']:
        print("  Passwords:", item['passwords'])
    if item['hashes']:
        print("  Passwords hashed in code:", item['hashes'])
    if item['user_inserts']:
        print("  User inserts:", item['user_inserts'])

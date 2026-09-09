import os
import re

files = ['order_module.html', 'customer_module.html', 'inventory_module.html', 'billing_module.html', 'logistics_module.html']

for f in files:
    path = os.path.join('d:\\dbmss\\templates', f)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Extract the modal block
        # It starts with "    <!-- CRUD Modal -->"
        # and ends with the first "    </div>\n{% endblock %}"
        # Let's just find the exact string to remove from title
        
        # Pattern to match everything from <!-- CRUD Modal --> to </div></div>
        pattern = re.compile(r'\s*<!-- CRUD Modal -->.*?</div>\s*</div>', re.DOTALL)
        
        match = pattern.search(content)
        if match:
            modal_code = match.group(0)
            
            # Remove it from its current position
            content = content.replace(modal_code, '')
            
            # Now we need to append it inside {% block content %}. 
            # Find the {% endblock %} that follows {% block content %}
            
            # A simple way is to insert it right before the FIRST {% endblock %} that appears AFTER {% block content %}
            # Or simpler: find the LAST </div> inside {% block content %}
            # Let's split by {% block content %}
            parts = content.split('{% block content %}')
            if len(parts) > 1:
                after_content = parts[1]
                # Split after_content by {% endblock %}
                endblock_parts = after_content.split('{% endblock %}')
                
                # The first part is the body of block content
                # Append modal_code to the end of the body
                endblock_parts[0] = endblock_parts[0] + "\n" + modal_code + "\n"
                
                # Reconstruct after_content
                after_content = '{% endblock %}'.join(endblock_parts)
                
                # Reconstruct full content
                new_content = parts[0] + '{% block content %}' + after_content
                
                with open(path, 'w', encoding='utf-8') as file:
                    file.write(new_content)
                print(f"Fixed {f}")
        else:
            print(f"Modal not found in {f}")

import os
import re

file_path = 'd:/dbmss/templates/shop_profile.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add IDs to inputs
content = content.replace('input type="text" value="Test"', 'input type="text" id="profile-first" value="Test"')
content = content.replace('input type="text" value="Customer"', 'input type="text" id="profile-last" value="Customer"')
content = content.replace('input type="email" value="customer@heritage.com"', 'input type="email" id="profile-email" value="customer@heritage.com"')
content = content.replace('input type="tel" value="+91 9876543210"', 'input type="tel" id="profile-phone" value="+91 9876543210"')
content = content.replace('<select class="w-full bg-[#111]', '<select id="profile-method" class="w-full bg-[#111]')

# Change form action
content = content.replace('<form class="space-y-6" onsubmit="event.preventDefault(); window.showToast(\'Profile updated successfully!\');">',
                          '<form class="space-y-6" onsubmit="event.preventDefault(); saveProfile();">')

# Add IDs to dynamic name displays
content = content.replace('<h3 class="text-2xl font-serif text-white mb-1">{{ session.get(\'name\', \'Test Customer\') }}</h3>',
                          '<h3 id="display-name" class="text-2xl font-serif text-white mb-1">{{ session.get(\'name\', \'Test Customer\') }}</h3>')
content = content.replace('<span class="text-3xl text-brand-gold font-serif">TC</span>',
                          '<span id="display-initials" class="text-3xl text-brand-gold font-serif">TC</span>')

js_script = """
    // Profile Management Logic
    function loadProfile() {
        const profile = JSON.parse(localStorage.getItem('userProfile'));
        if (profile) {
            document.getElementById('profile-first').value = profile.first || '';
            document.getElementById('profile-last').value = profile.last || '';
            document.getElementById('profile-email').value = profile.email || '';
            document.getElementById('profile-phone').value = profile.phone || '';
            document.getElementById('profile-method').value = profile.method || 'Email';
            updateNameDisplays(profile.first, profile.last);
        }
    }

    function saveProfile() {
        const profile = {
            first: document.getElementById('profile-first').value,
            last: document.getElementById('profile-last').value,
            email: document.getElementById('profile-email').value,
            phone: document.getElementById('profile-phone').value,
            method: document.getElementById('profile-method').value
        };
        localStorage.setItem('userProfile', JSON.stringify(profile));
        updateNameDisplays(profile.first, profile.last);
        window.showToast('Profile updated successfully!');
    }

    function updateNameDisplays(first, last) {
        if(first || last) {
            document.getElementById('display-name').innerText = `${first} ${last}`.trim();
            const initials = `${first ? first.charAt(0) : ''}${last ? last.charAt(0) : ''}`.toUpperCase();
            document.getElementById('display-initials').innerText = initials || 'TC';
        }
    }

    document.addEventListener("DOMContentLoaded", loadProfile);
</script>
"""

content = content.replace('</script>', js_script)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Profile logic updated.")

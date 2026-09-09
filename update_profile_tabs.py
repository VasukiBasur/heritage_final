import os

file_path = 'd:/dbmss/templates/shop_profile.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Update navigation links
old_nav_1 = '<a href="#" class="flex items-center space-x-3 p-3 rounded-xl bg-brand-gold/10 text-brand-gold border border-brand-gold/30">'
new_nav_1 = '<a href="#" id="nav-personal" onclick="event.preventDefault(); switchTab(\'personal\')" class="nav-tab-btn flex items-center space-x-3 p-3 rounded-xl bg-brand-gold/10 text-brand-gold border border-brand-gold/30">'
content = content.replace(old_nav_1, new_nav_1)

old_nav_2 = '<a href="#" class="flex items-center space-x-3 p-3 rounded-xl text-gray-400 hover:text-white hover:bg-[#1a1a1a] transition-colors">\n                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path></svg>\n                        <span class="text-sm font-medium">Addresses</span>\n                    </a>'
new_nav_2 = '<a href="#" id="nav-addresses" onclick="event.preventDefault(); switchTab(\'addresses\')" class="nav-tab-btn flex items-center space-x-3 p-3 rounded-xl text-gray-400 hover:text-white hover:bg-[#1a1a1a] transition-colors border border-transparent">\n                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path></svg>\n                        <span class="text-sm font-medium">Addresses</span>\n                    </a>'
content = content.replace(old_nav_2, new_nav_2)

old_nav_3 = '<a href="#" class="flex items-center space-x-3 p-3 rounded-xl text-gray-400 hover:text-white hover:bg-[#1a1a1a] transition-colors">\n                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path></svg>\n                        <span class="text-sm font-medium">Security</span>\n                    </a>'
new_nav_3 = '<a href="#" id="nav-security" onclick="event.preventDefault(); switchTab(\'security\')" class="nav-tab-btn flex items-center space-x-3 p-3 rounded-xl text-gray-400 hover:text-white hover:bg-[#1a1a1a] transition-colors border border-transparent">\n                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path></svg>\n                        <span class="text-sm font-medium">Security</span>\n                    </a>'
content = content.replace(old_nav_3, new_nav_3)

old_nav_4 = '<a href="#" class="flex items-center space-x-3 p-3 rounded-xl text-gray-400 hover:text-white hover:bg-[#1a1a1a] transition-colors">\n                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"></path></svg>\n                        <span class="text-sm font-medium">Notifications</span>\n                    </a>'
new_nav_4 = '<a href="#" id="nav-notifications" onclick="event.preventDefault(); switchTab(\'notifications\')" class="nav-tab-btn flex items-center space-x-3 p-3 rounded-xl text-gray-400 hover:text-white hover:bg-[#1a1a1a] transition-colors border border-transparent">\n                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"></path></svg>\n                        <span class="text-sm font-medium">Notifications</span>\n                    </a>'
content = content.replace(old_nav_4, new_nav_4)

# Wrap existing content in tab-personal
old_main_area = '<div class="lg:col-span-3">\n            <div class="glass-panel p-8 rounded-2xl border border-gray-800">'
new_main_area = """<div class="lg:col-span-3 relative">
            <!-- Personal Information Tab -->
            <div id="tab-personal" class="profile-tab glass-panel p-8 rounded-2xl border border-gray-800 transition-opacity duration-300 block">"""
content = content.replace(old_main_area, new_main_area)

# The end of the personal block is right before </div>\n        </div>\n        \n    </div>\n\n</div>\n\n<!-- Toast Notification Container -->
old_end_block = '</div>\n        </div>\n        \n    </div>\n\n</div>\n\n<!-- Toast Notification Container -->'
new_end_block = """</div>
            
            <!-- Addresses Tab -->
            <div id="tab-addresses" class="profile-tab glass-panel p-8 rounded-2xl border border-gray-800 transition-opacity duration-300 hidden">
                <div class="flex items-center justify-between mb-8 border-b border-gray-800 pb-8">
                    <div>
                        <h3 class="text-2xl font-serif text-white mb-1">Saved Addresses</h3>
                        <p class="text-sm text-gray-400">Manage your shipping and billing addresses</p>
                    </div>
                    <button class="px-4 py-2 bg-[#1a1a1a] border border-gray-700 text-brand-gold rounded hover:text-yellow-500 transition-colors text-sm font-bold">+ Add New Address</button>
                </div>
                
                <div class="space-y-4">
                    <div class="p-6 rounded-xl border border-brand-gold/30 bg-[#111] relative">
                        <div class="absolute top-6 right-6">
                            <span class="px-3 py-1 bg-brand-gold/20 text-brand-gold text-xs font-bold rounded-full">Default</span>
                        </div>
                        <h4 class="text-white font-bold mb-2">Home</h4>
                        <p class="text-sm text-gray-300 leading-relaxed mb-4">
                            123 Heritage Lane, Apt 4B<br>
                            Banjara Hills<br>
                            Hyderabad, Telangana 500034<br>
                            India
                        </p>
                        <div class="flex space-x-4 text-sm font-bold">
                            <button class="text-gray-400 hover:text-white transition-colors">Edit</button>
                            <button class="text-gray-400 hover:text-red-500 transition-colors">Remove</button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Security Tab -->
            <div id="tab-security" class="profile-tab glass-panel p-8 rounded-2xl border border-gray-800 transition-opacity duration-300 hidden">
                <div class="mb-8 border-b border-gray-800 pb-8">
                    <h3 class="text-2xl font-serif text-white mb-1">Security Settings</h3>
                    <p class="text-sm text-gray-400">Manage your password and security preferences</p>
                </div>
                
                <form class="space-y-6" onsubmit="event.preventDefault(); window.showToast('Password updated successfully!'); this.reset();">
                    <div class="space-y-4 max-w-md">
                        <div class="space-y-2">
                            <label class="text-xs text-gray-400 uppercase tracking-wider font-bold">Current Password</label>
                            <input type="password" class="w-full bg-[#111] border border-gray-700 rounded-lg py-3 px-4 text-white focus:outline-none focus:border-brand-gold transition-colors" required>
                        </div>
                        <div class="space-y-2">
                            <label class="text-xs text-gray-400 uppercase tracking-wider font-bold">New Password</label>
                            <input type="password" class="w-full bg-[#111] border border-gray-700 rounded-lg py-3 px-4 text-white focus:outline-none focus:border-brand-gold transition-colors" required>
                        </div>
                        <div class="space-y-2">
                            <label class="text-xs text-gray-400 uppercase tracking-wider font-bold">Confirm New Password</label>
                            <input type="password" class="w-full bg-[#111] border border-gray-700 rounded-lg py-3 px-4 text-white focus:outline-none focus:border-brand-gold transition-colors" required>
                        </div>
                        <button type="submit" class="mt-4 px-6 py-2 rounded-lg bg-[#1a1a1a] border border-gray-700 text-white hover:bg-gray-800 transition-colors font-bold text-sm">Update Password</button>
                    </div>
                </form>
            </div>

            <!-- Notifications Tab -->
            <div id="tab-notifications" class="profile-tab glass-panel p-8 rounded-2xl border border-gray-800 transition-opacity duration-300 hidden">
                <div class="mb-8 border-b border-gray-800 pb-8">
                    <h3 class="text-2xl font-serif text-white mb-1">Notification Preferences</h3>
                    <p class="text-sm text-gray-400">Control what updates you receive from us</p>
                </div>
                
                <div class="space-y-6">
                    <div class="flex items-center justify-between p-4 bg-[#111] rounded-xl border border-gray-800">
                        <div>
                            <h4 class="text-white font-bold mb-1">Order Updates</h4>
                            <p class="text-xs text-gray-400">Get notified when your order status changes</p>
                        </div>
                        <label class="relative inline-flex items-center cursor-pointer">
                            <input type="checkbox" value="" class="sr-only peer" checked onchange="window.showToast('Preferences saved')">
                            <div class="w-11 h-6 bg-gray-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-green-500"></div>
                        </label>
                    </div>
                    
                    <div class="flex items-center justify-between p-4 bg-[#111] rounded-xl border border-gray-800">
                        <div>
                            <h4 class="text-white font-bold mb-1">Promotional Emails</h4>
                            <p class="text-xs text-gray-400">Receive offers and heritage collection updates</p>
                        </div>
                        <label class="relative inline-flex items-center cursor-pointer">
                            <input type="checkbox" value="" class="sr-only peer" onchange="window.showToast('Preferences saved')">
                            <div class="w-11 h-6 bg-gray-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-green-500"></div>
                        </label>
                    </div>
                </div>
            </div>

        </div>
        
    </div>

</div>

<!-- Toast Notification Container -->"""
content = content.replace(old_end_block, new_end_block)


js_addition = """
    // Tab Switching Logic
    window.switchTab = function(tabId) {
        // Hide all tabs
        const tabs = document.querySelectorAll('.profile-tab');
        tabs.forEach(tab => {
            tab.classList.add('hidden');
            tab.classList.remove('block');
        });

        // Show selected tab
        const selectedTab = document.getElementById('tab-' + tabId);
        if (selectedTab) {
            selectedTab.classList.remove('hidden');
            selectedTab.classList.add('block');
        }

        // Reset nav styles
        const navBtns = document.querySelectorAll('.nav-tab-btn');
        navBtns.forEach(btn => {
            btn.classList.remove('bg-brand-gold/10', 'text-brand-gold', 'border-brand-gold/30');
            btn.classList.add('text-gray-400', 'border-transparent');
        });

        // Apply active style to selected nav
        const activeNav = document.getElementById('nav-' + tabId);
        if (activeNav) {
            activeNav.classList.remove('text-gray-400', 'border-transparent');
            activeNav.classList.add('bg-brand-gold/10', 'text-brand-gold', 'border-brand-gold/30');
        }
    };
"""

content = content.replace('// Profile Management Logic', js_addition + '\n    // Profile Management Logic')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Profile tabs logic updated.")

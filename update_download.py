import os

file_path = 'd:/dbmss/templates/shop_payment.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the onclick handler for the download button
old_button = '<button onclick="window.showToast(\'Statement download started.\')" class="px-3 py-1 bg-[#1a1a1a] border border-gray-700 rounded text-xs text-gray-300 hover:text-white transition-colors cursor-pointer">Download Statement</button>'
new_button = '<button onclick="downloadStatement()" class="px-3 py-1 bg-[#1a1a1a] border border-gray-700 rounded text-xs text-gray-300 hover:text-white transition-colors cursor-pointer">Download Statement</button>'
content = content.replace(old_button, new_button)

# Add the downloadStatement JS function
js_to_add = """
    window.downloadStatement = function() {
        const csvContent = "Date,Order ID,Payment Method,Amount\\n"
            + "May 28 2026,ORD-8921,Visa ending in 4242,24000\\n"
            + "May 15 2026,ORD-8850,Mastercard ending in 5555,18500\\n";
            
        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const url = URL.createObjectURL(blob);
        
        const link = document.createElement("a");
        link.setAttribute("href", url);
        link.setAttribute("download", "Heritage_Handloom_Statement.csv");
        link.style.visibility = 'hidden';
        
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        window.showToast("Statement downloaded successfully!");
    };
"""

content = content.replace('document.addEventListener("DOMContentLoaded", () => {', js_to_add + '\n    document.addEventListener("DOMContentLoaded", () => {')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Download logic updated.")

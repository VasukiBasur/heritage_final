import re

app_file = r"d:\dbmss\templates\dashboard.html"

with open(app_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix artisanChart binding back to total_logs
artisan_block = content.find("fetch('/api/stats/artisan_performance')")
if artisan_block != -1:
    end_block = content.find("fetch('/api/stats/order_status')", artisan_block)
    if end_block == -1:
        end_block = len(content)
        
    old_code = content[artisan_block:end_block]
    new_code = old_code.replace("item.count", "item.total_logs")
    content = content[:artisan_block] + new_code + content[end_block:]

# Revert fetch URL for status chart
content = content.replace("fetch('/api/stats/order_status')", "fetch('/api/stats/status_distribution')")

with open(app_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("Reverted bindings.")

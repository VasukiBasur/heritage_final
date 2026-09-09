import re

with open('templates/supplier_schedule.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update the parent container to allow horizontal scrolling
text = text.replace(
    'class="bg-[#141414] rounded-xl border border-[#d4af37]/20 shadow-2xl overflow-hidden mb-10"',
    'class="bg-[#141414] rounded-xl border border-[#d4af37]/20 shadow-2xl overflow-x-auto overflow-y-hidden custom-scrollbar mb-10"'
)

# 2. Wrap the grid inside a min-w-[1200px] div
text = text.replace(
    '<!-- Header row showing Days -->',
    '<div class="min-w-[1200px]">\n    <!-- Header row showing Days -->'
)

# 3. Close the new wrapper div at the end of the calendar grid body
text = text.replace(
    '        <!-- Sunday Column -->\n        <div class="p-2 space-y-3 bg-[#0a0a0a]">\n            <!-- Empty -->\n        </div>\n    </div>\n</div>',
    '        <!-- Sunday Column -->\n        <div class="p-2 space-y-3 bg-[#0a0a0a]">\n            <!-- Empty -->\n        </div>\n    </div>\n</div>\n</div>'
)

# Also fix the styling of the time/edit section so it doesn't wrap weirdly
text = text.replace(
    '<div class="flex justify-between items-start mb-2">',
    '<div class="flex justify-between items-center mb-2">'
)

with open('templates/supplier_schedule.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Fixed layout successfully.')

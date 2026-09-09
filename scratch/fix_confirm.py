import re

with open('templates/supplier_schedule.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add ID to the calendar body to avoid query selector escaping issues
text = text.replace('class="grid grid-cols-7 h-[600px] divide-x divide-[#d4af37]/10 overflow-y-auto custom-scrollbar"', 'id="calendar-grid-body" class="grid grid-cols-7 h-[600px] divide-x divide-[#d4af37]/10 overflow-y-auto custom-scrollbar"')

# 2. Add Edit button svg to the generateCardHTML function
edit_svg = '''
<button class="text-[#d4af37]/40 hover:text-[#d4af37] transition-colors" title="Edit">
    <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path></svg>
</button>
'''
edit_svg_escaped = edit_svg.replace('\n', '')

# Replace existing generateCardHTML logic to inject this button next to the time
new_js_start = f"""
    function generateCardHTML(item) {{
        let editBtn = `{edit_svg_escaped}`;
"""
text = re.sub(r'function generateCardHTML\(item\) \{', new_js_start, text)

# Insert editBtn into the returned HTML strings right next to the time span
text = text.replace('</span>\n                    <span class="w-2', f'</span>{edit_svg_escaped}\n                    </div>\n                    <div class="flex items-center"><span class="w-2')
# Wait, let's just do a simpler replacement for the flex container
text = text.replace('</span>\n                    <span class="w-2', f'</span>\n                    <div class="flex items-center space-x-2">{edit_svg_escaped}<span class="w-2')
text = text.replace('rounded-full bg-blue-500"></span>\n                </div>', 'rounded-full bg-blue-500"></span></div>\n                </div>')
text = text.replace('rounded-full bg-[#d4af37] animate-pulse"></span>\n                </div>', 'rounded-full bg-[#d4af37] animate-pulse"></span></div>\n                </div>')
text = text.replace('rounded-full bg-gray-500"></span>\n                </div>', 'rounded-full bg-gray-500"></span></div>\n                </div>')
text = text.replace('rounded-full bg-red-500"></span>\n                </div>', 'rounded-full bg-red-500"></span></div>\n                </div>')


# 3. Update querySelectors to use the new ID
text = re.sub(r"document\.querySelector.*?\.h-.*?(?:\]|\\\]|\\\\\\\])\]'\)", "document.getElementById('calendar-grid-body')", text)
text = re.sub(r"document\.querySelectorAll.*?\.h-.*?(?:\]|\\\]|\\\\\\\])\] > div'\)", "document.getElementById('calendar-grid-body').children", text)

# Make sure confirmSchedule works and pulls data from the form
new_confirm = f"""
    function confirmSchedule() {{
        const fridayCol = document.getElementById('calendar-grid-body').children[4];
        
        // Grab form values
        const hubSelect = document.querySelector('#schedule-modal-content select').value;
        const timeInput = document.querySelector('#schedule-modal-content input[type="time"]').value || "09:00 AM";
        const fleetSelect = document.querySelectorAll('#schedule-modal-content select')[1].value;

        // format time 09:00 -> 09:00 AM
        let timeStr = timeInput;
        if(timeInput.length === 5) {{ // basic formatting
           let hr = parseInt(timeInput.split(':')[0]);
           let min = timeInput.split(':')[1];
           let ampm = hr >= 12 ? 'PM' : 'AM';
           hr = hr % 12;
           hr = hr ? hr : 12;
           timeStr = hr.toString().padStart(2, '0') + ':' + min + ' ' + ampm;
        }}

        const newCard = document.createElement('div');
        newCard.className = 'bg-[#1a1a1a] border border-green-500/30 p-3 rounded-lg shadow-md mb-3 opacity-0 transform scale-95 transition-all duration-500';
        newCard.innerHTML = `
            <div class="flex justify-between items-start mb-2">
                <span class="text-[9px] text-green-400 uppercase tracking-widest font-bold">${{timeStr}}</span>
                <div class="flex items-center space-x-2">
                    {edit_svg_escaped}
                    <span class="w-2 h-2 rounded-full bg-green-500"></span>
                </div>
            </div>
            <h5 class="text-sm font-semibold text-[#f5ebd7]">${{hubSelect}}</h5>
            <p class="text-xs text-[#f5ebd7]/60 mt-1">${{fleetSelect.split(' ')[0]}}</p>
        `;
        
        // The last child in Friday column is the 'Schedule New' button
        // So we insert before the last child
        fridayCol.insertBefore(newCard, fridayCol.lastElementChild);
        
        closeScheduleModal();
        
        setTimeout(() => {{
            newCard.classList.remove('opacity-0', 'scale-95');
        }}, 350);
    }}
"""
text = re.sub(r'function confirmSchedule\(\) \{.*?\}\s*</script>', new_confirm + '\n</script>', text, flags=re.DOTALL)


with open('templates/supplier_schedule.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated supplier_schedule.html successfully.')

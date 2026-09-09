with open('templates/supplier_schedule.html', 'r', encoding='utf-8') as f:
    text = f.read()

load_js = """
    async function loadPersistedSchedules() {
        try {
            const response = await fetch('/supplier/schedule/api/list');
            const result = await response.json();
            
            if (result.success && result.data.length > 0) {
                result.data.forEach(schedule => {
                    const d = new Date(schedule.dispatch_date);
                    let day = d.getDay();
                    let colIndex = day === 0 ? 6 : day - 1;
                    
                    let timeStr = schedule.dispatch_time;
                    if(timeStr.length === 5) {
                       let hr = parseInt(timeStr.split(':')[0]);
                       let min = timeStr.split(':')[1];
                       let ampm = hr >= 12 ? 'PM' : 'AM';
                       hr = hr % 12;
                       hr = hr ? hr : 12;
                       timeStr = hr.toString().padStart(2, '0') + ':' + min + ' ' + ampm;
                    }
                    
                    const targetCol = document.getElementById('calendar-grid-body').children[colIndex];
                    if (targetCol) {
                        const newCard = document.createElement('div');
                        newCard.className = 'bg-[#1a1a1a] border border-green-500/30 p-3 rounded-lg shadow-md mb-3 group';
                        newCard.innerHTML = `
                            <div class="flex justify-between items-center mb-2">
                                <span class="text-[9px] text-green-400 uppercase tracking-widest font-bold">${timeStr}</span>
                                <span class="w-2 h-2 rounded-full bg-green-500"></span>
                            </div>
                            <h5 class="text-sm font-semibold text-[#f5ebd7]">${schedule.hub_name}</h5>
                            <p class="text-xs text-[#f5ebd7]/60 mt-1">${schedule.fleet_assigned.split(' ')[0]}</p>
                        `;
                        
                        const lastChild = targetCol.lastElementChild;
                        if (lastChild && lastChild.innerText && lastChild.innerText.includes('SCHEDULE NEW')) {
                            targetCol.insertBefore(newCard, lastChild);
                        } else {
                            targetCol.appendChild(newCard);
                        }
                    }
                });
            }
        } catch (e) {
            console.error('Error loading persisted schedules', e);
        }
    }
    
    document.addEventListener('DOMContentLoaded', loadPersistedSchedules);
    
    const originalChangeWeek = changeWeek;
    changeWeek = function(direction) {
        originalChangeWeek(direction);
        setTimeout(loadPersistedSchedules, 550);
    }
</script>
{% endblock %}
"""

with open('templates/supplier_schedule.html', 'w', encoding='utf-8') as f:
    f.write(text.strip() + '\n' + load_js)

print('Restored missing tags and functions successfully.')

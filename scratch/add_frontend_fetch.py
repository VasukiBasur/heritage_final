import re

with open('templates/supplier_schedule.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Update confirmSchedule to use fetch
new_confirm = """
    async function confirmSchedule() {
        const hubSelect = document.querySelector('#schedule-modal-content select').value;
        const dateInput = document.querySelector('#schedule-modal-content input[type="date"]').value;
        const timeInput = document.querySelector('#schedule-modal-content input[type="time"]').value || "09:00";
        const fleetSelect = document.querySelectorAll('#schedule-modal-content select')[1].value;

        try {
            const response = await fetch('/supplier/schedule/api/new', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    hub: hubSelect,
                    date: dateInput,
                    time: timeInput,
                    fleet: fleetSelect
                })
            });
            const result = await response.json();
            
            if (result.success) {
                // visually append it
                let timeStr = timeInput;
                if(timeInput.length === 5) {
                   let hr = parseInt(timeInput.split(':')[0]);
                   let min = timeInput.split(':')[1];
                   let ampm = hr >= 12 ? 'PM' : 'AM';
                   hr = hr % 12;
                   hr = hr ? hr : 12;
                   timeStr = hr.toString().padStart(2, '0') + ':' + min + ' ' + ampm;
                }
                
                let colIndex = 4;
                if(dateInput) {
                    const d = new Date(dateInput);
                    let day = d.getDay();
                    colIndex = day === 0 ? 6 : day - 1; 
                }

                const targetCol = document.getElementById('calendar-grid-body').children[colIndex];
                
                const newCard = document.createElement('div');
                newCard.className = 'bg-[#1a1a1a] border border-green-500/30 p-3 rounded-lg shadow-md mb-3 opacity-0 transform scale-95 transition-all duration-500 group';
                newCard.innerHTML = `
                    <div class="flex justify-between items-center mb-2">
                        <span class="text-[9px] text-green-400 uppercase tracking-widest font-bold">${timeStr}</span>
                        <span class="w-2 h-2 rounded-full bg-green-500"></span>
                    </div>
                    <h5 class="text-sm font-semibold text-[#f5ebd7]">${hubSelect}</h5>
                    <p class="text-xs text-[#f5ebd7]/60 mt-1">${fleetSelect.split(' ')[0]}</p>
                `;
                
                const lastChild = targetCol.lastElementChild;
                if (lastChild && lastChild.innerText && lastChild.innerText.includes('SCHEDULE NEW')) {
                    targetCol.insertBefore(newCard, lastChild);
                } else {
                    targetCol.appendChild(newCard);
                }
                
                setTimeout(() => {
                    newCard.classList.remove('opacity-0', 'scale-95');
                }, 50);
                
                closeScheduleModal();
            } else {
                alert('Failed to save schedule: ' + result.message);
            }
        } catch (e) {
            console.error(e);
            alert('An error occurred while saving.');
        }
    }
"""
text = re.sub(r'function confirmSchedule\(\) \{.*\}', new_confirm.strip(), text, flags=re.DOTALL)

# Add loadPersistedSchedules to the end of the script
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
    
    // Load persisted schedules initially
    document.addEventListener('DOMContentLoaded', loadPersistedSchedules);
    
    // Since changeWeek clears columns, we should hook loadPersistedSchedules into changeWeek as well
    // I will hook it via redefining the changeWeek timeout callback safely.
    const originalChangeWeek = changeWeek;
    changeWeek = function(direction) {
        originalChangeWeek(direction);
        setTimeout(loadPersistedSchedules, 550); // after the 500ms timeout of changeWeek
    }
</script>
"""

text = text.replace('</script>', load_js)

with open('templates/supplier_schedule.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated supplier_schedule.html for frontend DB integration.')

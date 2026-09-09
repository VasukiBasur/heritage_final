import re

with open('templates/supplier_schedule.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update the edit button to have an onclick handler
edit_btn_old = '<button class="text-[#d4af37]/40 hover:text-[#d4af37] transition-colors" title="Edit"><svg'
edit_btn_new = '<button onclick="openEditModal(event, this)" class="text-[#d4af37]/40 hover:text-[#d4af37] transition-colors" title="Edit"><svg'
text = text.replace(edit_btn_old, edit_btn_new)

# 2. Add openEditModal function and update confirmSchedule to place in correct column based on date
new_js = """
    // Modal Handling
    let editingCard = null;

    function openScheduleModal() {
        editingCard = null; // Reset
        document.querySelector('#schedule-modal-content h3').innerText = 'Schedule Dispatch';
        const modal = document.getElementById('schedule-modal');
        const content = document.getElementById('schedule-modal-content');
        modal.classList.remove('opacity-0', 'pointer-events-none');
        modal.classList.add('opacity-100');
        setTimeout(() => {
            content.classList.remove('scale-95', 'opacity-0');
            content.classList.add('scale-100', 'opacity-100');
        }, 50);
    }

    function openEditModal(event, btn) {
        event.stopPropagation(); // prevent card click
        editingCard = btn.closest('.group'); // Find the card div
        
        // Populate modal with card data
        const hubName = editingCard.querySelector('h5').innerText;
        const timeText = editingCard.querySelector('.text-\\\\[9px\\\\]').innerText;
        
        document.querySelector('#schedule-modal-content h3').innerText = 'Edit Dispatch';
        
        // Try to set select value
        const hubSelect = document.querySelector('#schedule-modal-content select');
        for(let i=0; i<hubSelect.options.length; i++) {
            if(hubSelect.options[i].text.includes(hubName)) {
                hubSelect.selectedIndex = i;
                break;
            }
        }
        
        const modal = document.getElementById('schedule-modal');
        const content = document.getElementById('schedule-modal-content');
        modal.classList.remove('opacity-0', 'pointer-events-none');
        modal.classList.add('opacity-100');
        setTimeout(() => {
            content.classList.remove('scale-95', 'opacity-0');
            content.classList.add('scale-100', 'opacity-100');
        }, 50);
    }

    function closeScheduleModal() {
        const modal = document.getElementById('schedule-modal');
        const content = document.getElementById('schedule-modal-content');
        content.classList.remove('scale-100', 'opacity-100');
        content.classList.add('scale-95', 'opacity-0');
        setTimeout(() => {
            modal.classList.remove('opacity-100');
            modal.classList.add('opacity-0', 'pointer-events-none');
        }, 300);
    }

    function confirmSchedule() {
        // Grab form values
        const hubSelect = document.querySelector('#schedule-modal-content select').value;
        const dateInput = document.querySelector('#schedule-modal-content input[type="date"]').value;
        const timeInput = document.querySelector('#schedule-modal-content input[type="time"]').value || "09:00";
        const fleetSelect = document.querySelectorAll('#schedule-modal-content select')[1].value;

        // format time 09:00 -> 09:00 AM
        let timeStr = timeInput;
        if(timeInput.length === 5) {
           let hr = parseInt(timeInput.split(':')[0]);
           let min = timeInput.split(':')[1];
           let ampm = hr >= 12 ? 'PM' : 'AM';
           hr = hr % 12;
           hr = hr ? hr : 12;
           timeStr = hr.toString().padStart(2, '0') + ':' + min + ' ' + ampm;
        }
        
        // Calculate which column to place it in based on Date
        let colIndex = 4; // default Friday
        if(dateInput) {
            const d = new Date(dateInput);
            let day = d.getDay(); // 0 is Sunday, 1 is Monday... 6 is Saturday
            // Our columns: 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri, 5=Sat, 6=Sun
            colIndex = day === 0 ? 6 : day - 1; 
        }

        if (editingCard) {
            // Update existing card
            editingCard.querySelector('h5').innerText = hubSelect;
            editingCard.querySelector('.text-\\\\[9px\\\\]').innerText = timeStr;
            editingCard.querySelector('p').innerText = fleetSelect.split(' ')[0];
            
            // Move it to the new column if date changed
            const targetCol = document.getElementById('calendar-grid-body').children[colIndex];
            if (editingCard.parentElement !== targetCol) {
                targetCol.insertBefore(editingCard, targetCol.lastElementChild || targetCol.firstElementChild);
            }
        } else {
            // Create new card
            const targetCol = document.getElementById('calendar-grid-body').children[colIndex];
            
            const newCard = document.createElement('div');
            newCard.className = 'bg-[#1a1a1a] border border-green-500/30 p-3 rounded-lg shadow-md mb-3 opacity-0 transform scale-95 transition-all duration-500 group';
            newCard.innerHTML = `
                <div class="flex justify-between items-center mb-2">
                    <span class="text-[9px] text-green-400 uppercase tracking-widest font-bold">${timeStr}</span>
                    <div class="flex items-center space-x-2">
                        <button onclick="openEditModal(event, this)" class="text-[#d4af37]/40 hover:text-[#d4af37] transition-colors" title="Edit"><svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path></svg></button>
                        <span class="w-2 h-2 rounded-full bg-green-500"></span>
                    </div>
                </div>
                <h5 class="text-sm font-semibold text-[#f5ebd7]">${hubSelect}</h5>
                <p class="text-xs text-[#f5ebd7]/60 mt-1">${fleetSelect.split(' ')[0]}</p>
            `;
            
            // Insert it before the "Schedule New" button if it exists, otherwise just append
            const lastChild = targetCol.lastElementChild;
            if (lastChild && lastChild.innerText && lastChild.innerText.includes('SCHEDULE NEW')) {
                targetCol.insertBefore(newCard, lastChild);
            } else {
                targetCol.appendChild(newCard);
            }
            
            setTimeout(() => {
                newCard.classList.remove('opacity-0', 'scale-95');
            }, 50);
        }
        
        closeScheduleModal();
    }
"""

text = re.sub(r'// Modal Handling.*</script>', new_js + '</script>', text, flags=re.DOTALL)

# Add more mock data to the weekData object
more_data_js = """        "0": [
            // Current Week Data
            [ // Mon
                { time: "07:30 AM", location: "Bangalore North", vehicle: "Truck E", active: false, id: "#PK-8839" },
                { time: "09:00 AM", location: "Ilkal Center", vehicle: "Truck A", active: false, id: "#PK-8840" },
                { time: "02:00 PM", location: "Hubli Zone", vehicle: "Van 2", active: false, id: "#PK-8841" }
            ],
            [ // Tue (Today)
                { time: "08:15 AM", location: "Mysore Silk Coop", vehicle: "Van 3", active: false, id: "#PK-8845" },
                { time: "10:00 AM", location: "Bangalore South", vehicle: "Truck C", active: true, id: "#PK-8846" },
                { time: "01:00 PM", location: "Dharwad Port", vehicle: "Truck F", delayed: true, id: "#PK-8848" },
                { time: "04:00 PM", location: "Udupi Center", vehicle: "Truck D", upcoming: true, id: "#PK-8847" }
            ],
            [ // Wed
                { time: "08:30 AM", location: "Mysore Hub", vehicle: "Truck A", active: false, id: "#PK-8848" },
                { time: "11:00 AM", location: "Mangalore Port", vehicle: "Van 1 (Unassigned)", delayed: true, id: "#PK-8849" },
                { time: "03:45 PM", location: "Ilkal Center", vehicle: "Truck B", active: false, id: "#PK-8851" }
            ],
            [ // Thu
                { time: "09:00 AM", location: "Hubli Zone", vehicle: "Truck B", active: false, id: "#PK-8850" },
                { time: "12:30 PM", location: "Bangalore North", vehicle: "Van 2", active: false, id: "#PK-8852" }
            ],
            [ // Fri
                { time: "08:00 AM", location: "Udupi Center", vehicle: "Truck C", active: false, id: "#PK-8855" }
            ],
            [ // Sat
                { time: "10:00 AM", location: "Mangalore Port", vehicle: "Truck D", active: false, id: "#PK-8860" }
            ], // Sat
            []  // Sun
        ],"""

text = re.sub(r'"0": \[\s*// Current Week Data.*?\]\s*\],\s*"1":', more_data_js + '\n        "1":', text, flags=re.DOTALL)

with open('templates/supplier_schedule.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated logic successfully.')

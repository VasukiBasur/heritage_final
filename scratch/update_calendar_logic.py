import re

with open('templates/supplier_schedule.html', 'r', encoding='utf-8') as f:
    text = f.read()

new_script = """<script>
    // Week Changing Simulation with Data Swapping
    let currentWeekOffset = 0;
    
    // Mock Data for Different Weeks
    const weekData = {
        "-1": [
            // Previous Week Data
            [ // Mon
                { time: "10:00 AM", location: "Mysore Hub", vehicle: "Truck A", active: false, id: "#PK-8700" }
            ],
            [ // Tue
                { time: "01:00 PM", location: "Bangalore South", vehicle: "Van 1", active: false, id: "#PK-8701" },
                { time: "03:30 PM", location: "Udupi Center", vehicle: "Truck C", active: false, id: "#PK-8702" }
            ],
            [ // Wed
                { time: "09:15 AM", location: "Ilkal Center", vehicle: "Truck B", active: false, id: "#PK-8705" }
            ],
            [], // Thu
            [ // Fri
                { time: "11:00 AM", location: "Mangalore Port", vehicle: "Truck D", active: false, id: "#PK-8710" }
            ],
            [], // Sat
            []  // Sun
        ],
        "0": [
            // Current Week Data
            [ // Mon
                { time: "09:00 AM", location: "Ilkal Center", vehicle: "Truck A", active: false, id: "#PK-8840" },
                { time: "02:00 PM", location: "Hubli Zone", vehicle: "Van 2", active: false, id: "#PK-8841" }
            ],
            [ // Tue (Today)
                { time: "10:00 AM", location: "Bangalore South", vehicle: "Truck C", active: true, id: "#PK-8846" },
                { time: "04:00 PM", location: "Udupi Center", vehicle: "Truck D", upcoming: true, id: "#PK-8847" }
            ],
            [ // Wed
                { time: "08:30 AM", location: "Mysore Hub", vehicle: "Truck A", active: false, id: "#PK-8848" },
                { time: "11:00 AM", location: "Mangalore Port", vehicle: "Van 1 (Unassigned)", delayed: true, id: "#PK-8849" }
            ],
            [ // Thu
                { time: "09:00 AM", location: "Hubli Zone", vehicle: "Truck B", active: false, id: "#PK-8850" }
            ],
            [], // Fri
            [], // Sat
            []  // Sun
        ],
        "1": [
            // Next Week Data
            [ // Mon
                { time: "08:00 AM", location: "Udupi Center", vehicle: "Truck A", active: false, id: "#PK-8901" },
                { time: "02:30 PM", location: "Mysore Silk Coop", vehicle: "Truck B", active: false, id: "#PK-8902" },
                { time: "05:00 PM", location: "Bangalore South", vehicle: "Van 2", active: false, id: "#PK-8903" }
            ],
            [ // Tue
                { time: "09:00 AM", location: "Ilkal Center", vehicle: "Truck C", active: false, id: "#PK-8904" }
            ],
            [], // Wed
            [ // Thu
                { time: "10:30 AM", location: "Mangalore Port", vehicle: "Truck D", active: false, id: "#PK-8910" },
                { time: "04:00 PM", location: "Hubli Zone", vehicle: "Van 1", active: false, id: "#PK-8911" }
            ],
            [ // Fri
                { time: "01:00 PM", location: "Mysore Hub", vehicle: "Truck A", active: false, id: "#PK-8915" }
            ],
            [], // Sat
            []  // Sun
        ]
    };
    
    function generateCardHTML(item) {
        if (item.active) {
            return `
            <div class="bg-gradient-to-br from-[#2a1a1a] to-black border border-[#d4af37]/40 p-3 rounded-lg shadow-lg hover:border-[#d4af37] cursor-pointer transition-colors group relative z-10">
                <div class="flex justify-between items-start mb-2">
                    <span class="text-[9px] text-[#d4af37] uppercase tracking-widest font-bold">${item.time}</span>
                    <span class="w-2 h-2 rounded-full bg-[#d4af37] animate-pulse"></span>
                </div>
                <h5 class="text-sm font-semibold text-[#f5ebd7]">${item.location}</h5>
                <p class="text-xs text-[#f5ebd7]/60 mt-1">${item.vehicle}</p>
                <div class="mt-3 pt-2 border-t border-[#d4af37]/20 flex justify-between items-center">
                    <span class="text-[9px] text-[#f5ebd7]/50">ID: ${item.id}</span>
                    <span class="bg-[#d4af37]/20 text-[#d4af37] text-[8px] px-2 py-0.5 rounded border border-[#d4af37]/30">Active</span>
                </div>
            </div>`;
        } else if (item.upcoming) {
            return `
            <div class="bg-[#1a1a1a] border border-[#d4af37]/20 p-3 rounded-lg shadow-md hover:border-[#d4af37]/50 cursor-pointer transition-colors group relative z-10 mt-8">
                <div class="flex justify-between items-start mb-2">
                    <span class="text-[9px] text-[#f5ebd7]/60 uppercase tracking-widest font-bold">${item.time}</span>
                    <span class="w-2 h-2 rounded-full bg-gray-500"></span>
                </div>
                <h5 class="text-sm font-semibold text-[#f5ebd7]">${item.location}</h5>
                <p class="text-xs text-[#f5ebd7]/60 mt-1">${item.vehicle}</p>
                <div class="mt-3 pt-2 border-t border-[#d4af37]/10 flex justify-between items-center">
                    <span class="text-[9px] text-[#f5ebd7]/50">ID: ${item.id}</span>
                    <span class="bg-gray-800 text-gray-400 text-[8px] px-2 py-0.5 rounded border border-gray-600">Upcoming</span>
                </div>
            </div>`;
        } else if (item.delayed) {
            return `
            <div class="bg-[#1a1a1a] border border-red-500/20 p-3 rounded-lg shadow-md hover:border-red-500/50 cursor-pointer transition-colors group relative overflow-hidden">
                <div class="absolute right-0 top-0 w-8 h-8 bg-red-900/10 rounded-bl-full"></div>
                <div class="flex justify-between items-start mb-2">
                    <span class="text-[9px] text-[#ff9999] uppercase tracking-widest font-bold">${item.time}</span>
                    <span class="w-2 h-2 rounded-full bg-red-500"></span>
                </div>
                <h5 class="text-sm font-semibold text-[#f5ebd7]">${item.location}</h5>
                <p class="text-xs text-[#f5ebd7]/60 mt-1">${item.vehicle}</p>
            </div>`;
        } else {
            return `
            <div class="bg-[#1a1a1a] border border-blue-500/20 p-3 rounded-lg shadow-md hover:border-blue-500/50 cursor-pointer transition-colors group">
                <div class="flex justify-between items-start mb-2">
                    <span class="text-[9px] text-blue-400 uppercase tracking-widest font-bold">${item.time}</span>
                    <span class="w-2 h-2 rounded-full bg-blue-500"></span>
                </div>
                <h5 class="text-sm font-semibold text-[#f5ebd7]">${item.location}</h5>
                <p class="text-xs text-[#f5ebd7]/60 mt-1">${item.vehicle}</p>
            </div>`;
        }
    }

    function changeWeek(direction) {
        currentWeekOffset += direction;
        
        // Clamp for mock data (we only have -1, 0, 1)
        if (currentWeekOffset < -1) currentWeekOffset = -1;
        if (currentWeekOffset > 1) currentWeekOffset = 1;
        
        // Show loading state by fading out calendar body
        const calBody = document.querySelector('.h-\\\\[600px\\\\]');
        calBody.style.opacity = '0.3';
        calBody.style.pointerEvents = 'none';
        
        // Simulate network fetch
        setTimeout(() => {
            // Update the dates in the header
            const days = document.querySelectorAll('.grid-cols-7 > div > p.text-2xl');
            
            days.forEach((dayEl, index) => {
                let newDate = 26 + index + (currentWeekOffset * 7);
                let month = "OCT";
                
                if (newDate > 31) {
                    newDate -= 31;
                    month = "NOV";
                } else if (newDate < 1) {
                    newDate += 30; // approx
                    month = "SEP";
                }
                
                dayEl.innerText = newDate.toString().padStart(2, '0');
                dayEl.nextElementSibling.innerText = month;
            });

            // Update DOM columns with new Data
            const columns = document.querySelectorAll('.h-\\\\[600px\\\\] > div');
            const newWeek = weekData[currentWeekOffset.toString()];
            
            columns.forEach((col, index) => {
                col.innerHTML = ''; // clear current cards
                
                // Keep the current time line if it's the current week, tuesday
                if (currentWeekOffset === 0 && index === 1) {
                    col.innerHTML += `
                        <div class="absolute top-[40%] left-0 w-full h-[1px] bg-red-500/50 z-0"></div>
                        <div class="absolute top-[40%] -left-1 w-2 h-2 rounded-full bg-red-500 z-0"></div>
                        <span class="absolute top-[37.5%] right-2 text-[8px] text-red-500 font-bold uppercase tracking-widest z-0">Current Time</span>
                    `;
                }
                
                // Add cards
                newWeek[index].forEach(item => {
                    col.innerHTML += generateCardHTML(item);
                });
                
                // Add the schedule new button to Friday
                if (index === 4) {
                    col.innerHTML += `
                        <div onclick="openScheduleModal()" class="bg-gradient-to-br from-[#1a1a1a] to-black border border-[#d4af37]/20 p-3 rounded-lg shadow-md border-dashed cursor-pointer hover:border-[#d4af37]/50 transition-colors mt-3">
                            <div class="flex flex-col items-center justify-center h-24 text-center">
                                <svg class="w-6 h-6 text-[#d4af37]/30 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path></svg>
                                <span class="text-[10px] text-[#f5ebd7]/50 uppercase tracking-widest font-bold">Schedule New</span>
                            </div>
                        </div>
                    `;
                }
            });
            
            calBody.style.opacity = '1';
            calBody.style.pointerEvents = 'auto';
        }, 500);
    }

    // Modal Handling
    function openScheduleModal() {
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
        const fridayCol = document.querySelectorAll('.h-\\\\[600px\\\\] > div')[4];
        
        const newCard = document.createElement('div');
        newCard.className = 'bg-[#1a1a1a] border border-green-500/30 p-3 rounded-lg shadow-md opacity-0 transform scale-95 transition-all duration-500';
        newCard.innerHTML = `
            <div class="flex justify-between items-start mb-2">
                <span class="text-[9px] text-green-400 uppercase tracking-widest font-bold">09:00 AM</span>
                <span class="w-2 h-2 rounded-full bg-green-500"></span>
            </div>
            <h5 class="text-sm font-semibold text-[#f5ebd7]">New Pickup Scheduled</h5>
            <p class="text-xs text-[#f5ebd7]/60 mt-1">Truck A</p>
        `;
        
        // Insert before the last element (which is the schedule button)
        fridayCol.insertBefore(newCard, fridayCol.lastElementChild);
        
        closeScheduleModal();
        
        setTimeout(() => {
            newCard.classList.remove('opacity-0', 'scale-95');
        }, 350);
    }
</script>"""

pattern = re.compile(r'<script>.*</script>', re.DOTALL)
new_text = pattern.sub(new_script.strip(), text)

with open('templates/supplier_schedule.html', 'w', encoding='utf-8') as f:
    f.write(new_text)

print("Updated script logic successfully.")


        window.switchTab = function(tabId, element) {
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
            document.getElementById('tab-' + tabId).classList.add('active');
            
            if(element) {
                document.querySelectorAll('.nav-link').forEach(el => el.classList.remove('active', 'border-brand-gold', 'bg-brand-gold/10'));
                document.querySelectorAll('.nav-link').forEach(el => el.classList.add('border-transparent'));
                element.classList.remove('border-transparent');
                element.classList.add('active', 'border-brand-gold', 'bg-brand-gold/10');
            }
            
            // Scroll to top
            document.getElementById('main-scroll').scrollTop = 0;
        };

        window.showToast = function(message) {
            const toast = document.createElement('div');
            toast.className = 'bg-black/90 border border-brand-gold/50 shadow-lg text-white px-5 py-3 rounded-lg text-sm transition-opacity duration-300 opacity-0';
            toast.innerHTML = `<span class="flex items-center"><svg class="w-5 h-5 mr-2 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>${message}</span>`;
            const container = document.getElementById('toast-container');
            if(container) {
                container.appendChild(toast);
                setTimeout(() => toast.style.opacity = '1', 10);
                setTimeout(() => {
                    toast.style.opacity = '0';
                    setTimeout(() => toast.remove(), 400);
                }, 3000);
            }
        };

        // Initialize Charts
        document.addEventListener("DOMContentLoaded", () => {
            // Dashboard Combo Chart
            const ctx1 = document.getElementById('monthlyChart').getContext('2d');
            new Chart(ctx1, { type: 'bar', data: { labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'], datasets: [{ label: 'Deliveries', data: [120, 150, 140, 180, 210], backgroundColor: '#D4AF37', borderRadius: 4 }] }, options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { y: { display: false }, x: { grid: { display: false, drawBorder: false }, ticks: { color: '#666', font: {size: 10} } } } } });

            const ctx2 = document.getElementById('successChart').getContext('2d');
            new Chart(ctx2, { type: 'doughnut', data: { labels: ['Success', 'Failed'], datasets: [{ data: [99, 1], backgroundColor: ['#10B981', '#374151'], borderWidth: 0, cutout: '75%' }] }, options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } } } });

            const ctx3 = document.getElementById('earningsGrowthChart').getContext('2d');
            let grad3 = ctx3.createLinearGradient(0, 0, 0, 200); grad3.addColorStop(0, 'rgba(168, 85, 247, 0.5)'); grad3.addColorStop(1, 'rgba(168, 85, 247, 0.0)');
            new Chart(ctx3, { type: 'line', data: { labels: ['W1', 'W2', 'W3', 'W4'], datasets: [{ data: [4000, 5200, 4800, 6100], borderColor: '#A855F7', backgroundColor: grad3, borderWidth: 2, fill: true, pointRadius: 0, tension: 0.4 }] }, options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { y: { display: false }, x: { grid: { display: false, drawBorder: false }, ticks: { color: '#666', font: {size: 10} } } } } });

            // Earnings Tab Combo Chart
            const ctx4 = document.getElementById('earningsComboChart').getContext('2d');
            new Chart(ctx4, {
                type: 'bar',
                data: {
                    labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
                    datasets: [
                        {
                            type: 'line',
                            label: 'Earnings (₹)',
                            data: [8000, 9500, 11000, 12700],
                            borderColor: '#D4AF37',
                            borderWidth: 2,
                            tension: 0.4,
                            yAxisID: 'y1'
                        },
                        {
                            type: 'bar',
                            label: 'Deliveries',
                            data: [100, 115, 130, 150],
                            backgroundColor: 'rgba(255, 255, 255, 0.1)',
                            borderRadius: 4,
                            yAxisID: 'y'
                        }
                    ]
                },
                options: {
                    responsive: true, maintainAspectRatio: false,
                    plugins: { legend: { labels: { color: '#888' } } },
                    scales: {
                        x: { grid: { color: '#333' }, ticks: { color: '#888' } },
                        y: { position: 'left', grid: { color: '#333' }, ticks: { color: '#888' } },
                        y1: { position: 'right', grid: { drawOnChartArea: false }, ticks: { color: '#D4AF37' } }
                    }
                }
            });
        

        // Delivery Messages Logic
        let currentDelContact = 'hq';
        
        const defaultDelChats = {
            hq: [
                { sender: 'other', text: 'Hello Rahul, we noticed a delay on your route to Jubilee Hills. Are you facing traffic on route 4?', time: '10:45 AM' },
                { sender: 'me', text: 'Yes, there\'s a roadblock near the main intersection. I am taking the alternate route via the bypass. ETA updated to +10 mins.', time: '10:47 AM' },
                { sender: 'other', text: 'Copy that. Drive safe!', time: '10:48 AM' }
            ],
            anjali: [
                { sender: 'other', text: 'Hi, I might not be home. Please leave it with the security guard.', time: 'Yesterday' }
            ],
            weaver: [
                { sender: 'other', text: 'Package is ready for pickup at Gate B.', time: 'May 25' }
            ]
        };

        const delContactDetails = {
            hq: { name: 'HQ Logistics Support', status: 'Online', statusColor: 'green-500' },
            anjali: { name: 'Anjali Sharma (Customer)', status: 'Offline', statusColor: 'gray-500' },
            weaver: { name: 'Weaver Cooperative', status: 'Offline', statusColor: 'gray-500' }
        };

        window.switchDelContact = function(contactId) {
            currentDelContact = contactId;
            
            // Update Sidebar Styles
            document.getElementById('del-contact-hq').classList.remove('bg-[#1a1a1a]');
            document.getElementById('del-contact-anjali').classList.remove('bg-[#1a1a1a]');
            document.getElementById('del-contact-weaver').classList.remove('bg-[#1a1a1a]');
            document.getElementById('del-contact-' + contactId).classList.add('bg-[#1a1a1a]');
            
            // Update Header
            const details = delContactDetails[contactId];
            document.getElementById('del-chat-header-name').innerText = details.name;
            document.getElementById('del-chat-header-status').innerHTML = `<span class="w-2 h-2 rounded-full bg-${details.statusColor} mr-2"></span>${details.status}`;
            document.getElementById('del-chat-header-status').className = `text-xs text-${details.statusColor} flex items-center`;
            
            renderDelMessages();
        };

        function renderDelMessages() {
            let chats = JSON.parse(localStorage.getItem('delChats'));
            if (!chats || Object.keys(chats).length === 0) {
                chats = defaultDelChats;
                localStorage.setItem('delChats', JSON.stringify(chats));
            }

            const messages = chats[currentDelContact] || [];
            const container = document.getElementById('del-chat-messages');
            
            container.innerHTML = '<div class="flex justify-center mb-4"><span class="text-xs text-gray-600 bg-[#111] px-2 py-1 rounded">Conversation Started</span></div>';

            messages.forEach(msg => {
                const div = document.createElement('div');
                if (msg.sender === 'me') {
                    div.className = 'flex justify-end mb-4';
                    div.innerHTML = `
                        <div class="bg-brand-gold text-black rounded-2xl px-4 py-2 max-w-[70%] text-sm shadow-md">
                            <p>${msg.text}</p>
                            <span class="text-[10px] opacity-70 block text-right mt-1">${msg.time}</span>
                        </div>`;
                } else {
                    div.className = 'flex justify-start mb-4';
                    div.innerHTML = `
                        <div class="bg-[#1a1a1a] border border-gray-800 text-gray-300 rounded-2xl px-4 py-2 max-w-[70%] text-sm shadow-md">
                            <p>${msg.text}</p>
                            <span class="text-[10px] text-gray-500 block mt-1">${msg.time}</span>
                        </div>`;
                }
                container.appendChild(div);
            });
            
            container.scrollTop = container.scrollHeight;
        }

        window.sendDelMessage = function() {
            const input = document.getElementById('del-chat-input');
            const text = input.value.trim();
            if (!text) return;

            let chats = JSON.parse(localStorage.getItem('delChats')) || defaultDelChats;
            if (!chats[currentDelContact]) chats[currentDelContact] = [];
            
            const now = new Date();
            const timeStr = now.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
            
            chats[currentDelContact].push({ sender: 'me', text: text, time: timeStr });
            localStorage.setItem('delChats', JSON.stringify(chats));
            
            input.value = '';
            renderDelMessages();
        };

        document.addEventListener("DOMContentLoaded", () => {
            renderDelMessages();
            document.getElementById('del-chat-input').addEventListener('keypress', function (e) {
                if (e.key === 'Enter') {
                    sendDelMessage();
                }
            });
            });
    
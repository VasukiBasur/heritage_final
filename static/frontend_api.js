document.addEventListener('DOMContentLoaded', () => {
    const path = window.location.pathname;
    const tbody = document.querySelector('table tbody');
    const form = document.querySelector('form');

    function loadData(url, renderFunc) {
        if (!tbody) return;
        fetch(url)
            .then(res => res.json())
            .then(res => {
                if(res.success && res.data) {
                    tbody.innerHTML = '';
                    res.data.forEach(item => {
                        tbody.innerHTML += renderFunc(item);
                    });
                }
            })
            .catch(err => console.error("Error loading data:", err));
    }

    if (path.includes('product_catalog_module')) {
        loadData('/api/products', (item) => `
            <tr>
                <td>#PROD-${item.product_id}</td>
                <td class="font-bold text-brand-gold">${item.product_name}</td>
                <td>${item.category}</td>
                <td class="text-green-400 font-mono">₹${item.price}</td>
                <td class="text-blue-400">${item.stock_quantity}</td>
                <td>
                    <div class="flex items-center space-x-2">
                        <img src="https://api.qrserver.com/v1/create-qr-code/?size=50x50&data=${encodeURIComponent(window.location.origin + '/trace/' + item.product_id)}" class="w-8 h-8 rounded-sm bg-white p-0.5">
                        <a href="/trace/${item.product_id}" class="text-xs bg-brand-gold/10 text-brand-gold px-2 py-1 rounded border border-brand-gold/30 hover:bg-brand-gold hover:text-brand-black transition-colors">Trace</a>
                    </div>
                </td>
            </tr>
        `);
    } 
    else if (path.includes('order_module')) {
        loadData('/api/orders', (item) => `
            <tr>
                <td>#ORD-${item.order_id}</td>
                <td class="font-bold text-brand-gold">${item.customer_name}</td>
                <td>Multiple Items</td>
                <td class="text-blue-400">--</td>
                <td class="text-green-400 font-mono">₹${item.total_amount}</td>
                <td><span class="px-2 py-1 rounded-sm text-xs border border-brand-gold/30 bg-brand-gold/10 text-brand-gold">${item.status}</span></td>
                <td>${item.shipping_address || 'Pending'}</td>
            </tr>
        `);
    }
    else if (false) {
        loadData('/api/inventory', (item) => `
            <tr>
                <td>#MAT-${item.material_id}</td>
                <td class="font-bold text-brand-gold">${item.material_name}</td>
                <td>${item.quantity_available} Units</td>
                <td>
                    <button class="text-blue-400 hover:text-blue-300 mr-3">Restock</button>
                </td>
            </tr>
        `);
    }
    else if (false) {
        loadData('/api/suppliers', (item) => `
            <tr>
                <td>#SUP-${item.supplier_id}</td>
                <td class="font-bold text-brand-gold">${item.company_name}</td>
                <td>${item.contact_person}</td>
                <td>${item.phone}</td>
                <td>${item.material_type}</td>
                <td><span class="px-2 py-1 rounded text-[10px] uppercase tracking-wider bg-green-900/50 text-green-400 border border-current/20">${item.status}</span></td>
                <td><button class="text-blue-400 hover:text-blue-300">Edit</button></td>
            </tr>
        `);
    }
    else if (path.includes('billing_module')) {
        loadData('/api/payments', (item) => `
            <tr>
                <td>#TXN-${item.payment_id}</td>
                <td>#ORD-${item.order_id}</td>
                <td class="font-bold text-brand-gold">₹${item.amount}</td>
                <td>${item.payment_method || 'UPI'}</td>
                <td>${new Date(item.payment_date).toLocaleDateString()}</td>
                <td><span class="px-2 py-1 rounded text-[10px] uppercase tracking-wider ${item.transaction_status === 'Completed' ? 'bg-green-900/50 text-green-400' : 'bg-yellow-900/50 text-yellow-400'} border border-current/20">${item.transaction_status}</span></td>
            </tr>
        `);
    }
    else if (path.includes('logistics_module') || path.includes('shipment_dashboard')) {
        loadData('/api/shipments', (item) => `
            <tr>
                <td>#SHP-${item.shipment_id}</td>
                <td>#ORD-${item.order_id}</td>
                <td class="font-bold text-brand-gold">${item.customer_name}</td>
                <td>${item.shipping_address || 'Pending'}</td>
                <td><span class="px-2 py-1 rounded text-[10px] uppercase tracking-wider bg-blue-900/50 text-blue-400 border border-current/20">${item.current_status}</span></td>
                <td><button class="text-green-400 hover:text-green-300">Update Status</button></td>
            </tr>
        `);
    }

    if (form) {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            const formData = new FormData(form);
            const payload = Object.fromEntries(formData.entries());
            let apiUrl = '';

            if (path.includes('product_catalog_module')) apiUrl = '/api/products';
            else if (path.includes('order_module')) apiUrl = '/api/orders';
            else if (path.includes('supplier_module')) apiUrl = '/api/suppliers';
            
            if (apiUrl) {
                fetch(apiUrl, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                })
                .then(res => res.json())
                .then(res => {
                    if (res.success) {
                        alert("Added successfully!");
                        window.location.reload();
                    } else {
                        alert("Error: " + res.error);
                    }
                })
                .catch(err => alert("Network error: " + err));
            }
        });
    }

    if (path.includes('dashboard')) {
        fetch('/api/dashboard/stats')
            .then(res => res.json())
            .then(res => {
                if(res.success) {
                    const rev = document.getElementById('stat-revenue');
                    const ord = document.getElementById('stat-orders');
                    const art = document.getElementById('stat-artisans');
                    if (rev) rev.innerText = '₹' + res.data.revenue.toLocaleString();
                    if (ord) ord.innerText = res.data.orders.toLocaleString();
                    if (art) art.innerText = res.data.artisans.toLocaleString();
                }
            });
    }
});

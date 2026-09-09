/**
 * Artisan ERP Dashboard - Dynamic Fetch API Integration
 * Handles asynchronous operations for updating, deleting, and fetching data.
 */

const API_BASE = '/api/artisan'; // Adjust based on how blueprint is registered (could be /artisan/api/artisan)

// 1. Delete Product
async function deleteProduct(productId) {
    if (!confirm("Are you sure you want to delete this product from the marketplace?")) return;
    
    try {
        const response = await fetch(`${API_BASE}/products/${productId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const result = await response.json();
        
        if (response.ok) {
            alert(result.message);
            // Dynamically remove the card from the UI
            const card = document.getElementById(`product-card-${productId}`);
            if (card) {
                card.style.opacity = '0';
                setTimeout(() => card.remove(), 500);
            }
        } else {
            alert(result.error || "Failed to delete product.");
        }
    } catch (error) {
        console.error("Error:", error);
        alert("An error occurred while communicating with the server.");
    }
}

// 2. Load Dashboard Charts Dynamically
async function loadDashboardCharts() {
    try {
        const response = await fetch(`${API_BASE}/dashboard/stats`);
        if (!response.ok) return;
        
        const data = await response.json();
        const brandGold = '#d4af37';
        const brandLightGold = 'rgba(212, 175, 55, 0.4)';
        
        // Update Earnings Chart
        const earningsCtx = document.getElementById('earningsChart');
        if (earningsCtx && window.earningsChartInstance) {
            window.earningsChartInstance.data.labels = data.months;
            window.earningsChartInstance.data.datasets[0].data = data.earnings;
            window.earningsChartInstance.update();
        }
        
        // Update Production Chart
        const productionCtx = document.getElementById('productionChart');
        if (productionCtx && window.productionChartInstance) {
            window.productionChartInstance.data.labels = data.production.labels;
            window.productionChartInstance.data.datasets[0].data = data.production.active;
            window.productionChartInstance.data.datasets[1].data = data.production.completed;
            window.productionChartInstance.update();
        }
        
    } catch (error) {
        console.error("Failed to load dashboard data dynamically", error);
    }
}

// 3. Update Order Status
async function updateOrderStatus(orderId, newStatus) {
    try {
        const response = await fetch(`${API_BASE}/orders/${orderId}/status`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ status: newStatus })
        });
        
        const result = await response.json();
        if (response.ok) {
            // alert(result.message);
            // Update the DOM visually instead of reloading to persist mock changes
            const statusCell = document.getElementById(`status-${orderId}`);
            const actionsCell = document.getElementById(`actions-${orderId}`);
            if (statusCell && actionsCell) {
                if (newStatus === 'Processing') {
                    statusCell.innerHTML = `<span class="bg-blue-900/40 text-blue-400 text-[10px] font-bold uppercase tracking-widest px-3 py-1 rounded border border-blue-500/30">Processing</span>`;
                    actionsCell.innerHTML = `<button onclick="updateOrderStatus(${orderId}, 'Shipped')" class="bg-brand-gold/20 hover:bg-brand-gold/40 text-brand-gold border border-brand-gold/30 py-1 px-3 rounded text-xs font-bold uppercase tracking-widest transition-colors">Mark Shipped</button>`;
                } else if (newStatus === 'Cancelled') {
                    statusCell.innerHTML = `<span class="bg-red-900/40 text-red-400 text-[10px] font-bold uppercase tracking-widest px-3 py-1 rounded border border-red-500/30">Cancelled</span>`;
                    actionsCell.innerHTML = ``;
                } else if (newStatus === 'Shipped') {
                    statusCell.innerHTML = `<span class="bg-green-900/40 text-green-400 text-[10px] font-bold uppercase tracking-widest px-3 py-1 rounded border border-green-500/30">Shipped</span>`;
                    actionsCell.innerHTML = ``;
                }
            }
        } else {
            alert(result.error || "Failed to update order status.");
        }
    } catch (error) {
        console.error("Error:", error);
    }
}

// Initialize dynamic listeners on load
document.addEventListener("DOMContentLoaded", () => {
    // If we are on the dashboard page, load dynamic chart data
    if (document.getElementById('earningsChart')) {
        // loadDashboardCharts(); // Uncomment when APIs are fully populated
    }
});

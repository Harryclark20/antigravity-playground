async function fetchBotState() {
    try {
        const response = await fetch('/api/state');
        if (!response.ok) throw new Error('Network response was not ok');
        const data = await response.json();
        updateDashboard(data);
    } catch (error) {
        console.error('Failed to fetch bot state:', error);
        document.getElementById('status-text').innerText = "Disconnected";
        document.getElementById('status-dot').className = "dot error";
    }
}

function formatCurrency(value) {
    return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(value);
}

function updateDashboard(data) {
    // Status
    document.getElementById('status-text').innerText = data.status;
    const dot = document.getElementById('status-dot');
    if (data.status.includes('Running')) {
        dot.className = "dot running";
    } else {
        dot.className = "dot error";
    }

    // Metrics
    document.getElementById('balance-value').innerText = formatCurrency(data.balance);
    document.getElementById('equity-value').innerText = formatCurrency(data.equity);
    document.getElementById('tracking-value').innerText = data.symbols_tracking;

    // Table
    const tbody = document.getElementById('trades-body');
    if (data.open_trades.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="empty-state">Looking for high probability setups...</td></tr>';
    } else {
        tbody.innerHTML = '';
        data.open_trades.forEach(trade => {
            const tr = document.createElement('tr');

            const profitClass = trade.profit >= 0 ? "profit-pos" : "profit-neg";
            const typeStyle = trade.type === "BUY" ? "color: #58a6ff; font-weight: bold;" : "color: #f85149; font-weight: bold;";

            tr.innerHTML = `
                <td>#${trade.ticket}</td>
                <td><strong>${trade.symbol}</strong></td>
                <td style="${typeStyle}">${trade.type}</td>
                <td>${trade.volume.toFixed(2)}</td>
                <td>${trade.open_price.toFixed(5)}</td>
                <td>${trade.current_price.toFixed(5)}</td>
                <td class="${profitClass}">$${trade.profit.toFixed(2)}</td>
            `;
            tbody.appendChild(tr);
        });
    }
}

// Poll the server every 500ms for that true real-time HFT feel
setInterval(fetchBotState, 500);
fetchBotState();

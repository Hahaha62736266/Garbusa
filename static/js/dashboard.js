// Crop Distribution Chart
const cropCtx = document.getElementById('cropChart').getContext('2d');
new Chart(cropCtx, {
    type: 'doughnut',
    data: {
        labels: ['Rice', 'Corn', 'Vegetables', 'Coconut', 'Banana', 'Others'],
        datasets: [{
            data: [42, 23, 15, 10, 7, 3],
            backgroundColor: [
                '#2e7d32', '#43a047', '#66bb6a', '#9ccc65', '#d4e157', '#aed581'
            ],
            borderWidth: 0
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: { position: 'bottom' }
        }
    }
});

// Farmer Status Chart
const statusCtx = document.getElementById('statusChart').getContext('2d');
new Chart(statusCtx, {
    type: 'bar',
    data: {
        labels: ['Active', 'Pending', 'Inactive'],
        datasets: [{
            label: 'Farmers',
            data: [215, 22, 11],
            backgroundColor: ['#2e7d32', '#f59e0b', '#9ca3af'],
            borderRadius: 8
        }]
    },
    options: {
        responsive: true,
        plugins: { legend: { display: false } },
        scales: {
            y: { beginAtZero: true, grid: { display: false } },
            x: { grid: { display: false } }
        }
    }
});

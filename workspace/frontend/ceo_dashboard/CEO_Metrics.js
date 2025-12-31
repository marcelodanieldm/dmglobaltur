// CEO_Metrics.js
// MRR Chart with Transaction Fee Revenue
const ctx = document.getElementById('mrrChart').getContext('2d');
const mrrChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    datasets: [
      {
        label: 'MRR (Core Revenue)',
        data: [12000, 13500, 14200, 15000, 15800, 16500],
        borderColor: '#bfa14a',
        backgroundColor: 'rgba(191,161,74,0.08)',
        tension: 0.3,
        fill: true
      },
      {
        label: 'Transaction Fee Revenue',
        data: [320, 370, 410, 450, 480, 520],
        borderColor: '#e6c200',
        backgroundColor: 'rgba(230,194,0,0.10)',
        tension: 0.3,
        fill: true
      }
    ]
  },
  options: {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: false
      }
    }
  }
});

// Compliance: Generate Proof of Commission (PDF)
document.getElementById('generate-proof').onclick = function() {
  // Simulate PDF generation
  setTimeout(() => {
    document.getElementById('proof-status').innerText = 'Proof of Commission generated for all jurisdictions!';
  }, 1200);
};

document.addEventListener('DOMContentLoaded', () => {
    const ctx = document.getElementById("placesChart");
    if (ctx) {
        try {
            const labels = JSON.parse(ctx.dataset.labels || '[]');
            const values = JSON.parse(ctx.dataset.values || '[]');

            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: "Checkins by Month",
                        backgroundColor: '#195ddd',
                        borderColor: '#000',
                        data: values,
                    }]
                }
            });
        } catch (error) {
            console.error('Error initializing Checkins chart:', error);
        }
    }
});

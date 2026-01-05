document.addEventListener('DOMContentLoaded', () => {
    const ctx = document.getElementById("myqueenChart");
    if (ctx) {
        try {
            const labels = JSON.parse(ctx.dataset.labels || '[]');
            const values = JSON.parse(ctx.dataset.values || '[]');

            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: "Songs played by Queen per Month",
                        backgroundColor: '#195ddd',
                        borderColor: '#000',
                        data: values,
                    }]
                }
            });
        } catch (error) {
            console.error('Error initializing Queen chart:', error);
        }
    }
});

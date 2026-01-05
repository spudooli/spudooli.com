document.addEventListener('DOMContentLoaded', () => {
    const ctx = document.getElementById("myChart");
    if (ctx) {
        try {
            const labels = JSON.parse(ctx.dataset.labels || '[]');
            const values = JSON.parse(ctx.dataset.values || '[]');

            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: "$ Spend on Charging the EV by Month",
                        backgroundColor: '#000',
                        borderColor: '#000',
                        data: values,
                    }]
                }
            });
        } catch (error) {
            console.error('Error initializing BMW i3 chart:', error);
        }
    }
});

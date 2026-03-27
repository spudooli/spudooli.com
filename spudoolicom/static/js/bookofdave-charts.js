document.addEventListener('DOMContentLoaded', () => {
    const ctx = document.getElementById("mypostsChart");
    if (ctx) {
        try {
            const labels = JSON.parse(ctx.dataset.labels || '[]');
            const values = JSON.parse(ctx.dataset.values || '[]');

            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: "Posts per month",
                        backgroundColor: '#195ddd',
                        borderColor: '#000',
                        data: values,
                    }]
                }
            });
        } catch (error) {
            console.error('Error initializing Book of Dave chart:', error);
        }
    }
});

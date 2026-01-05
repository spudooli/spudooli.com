document.addEventListener('DOMContentLoaded', () => {

    const initChart = (canvasId, label) => {
        const canvas = document.getElementById(canvasId);
        if (!canvas) return;

        try {
            // Helper to get data, handling potential issues with how data is embedded
            const getData = (attr) => {
                if (!canvas.dataset[attr]) return [];
                return JSON.parse(canvas.dataset[attr]);
            };

            const labels = getData('labels');
            const values = getData('values');

            if (!labels.length && !values.length) {
                console.warn(`No data found for chart ${canvasId}`);
                return;
            }

            new Chart(canvas, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: label,
                        backgroundColor: '#195ddd',
                        borderColor: '#000',
                        data: values,
                    }]
                }
            });
        } catch (error) {
            console.error('Error initializing chart for:', canvasId, error);
        }
    };

    // Initialize all charts
    initChart("myChart", "$ Spend on Petrol by Month");
    initChart("myWarehouseChart", "$ Spend at The Warehouse by Month");
    initChart("myhardwareChart", "$ Spend at all hardware stores by Month");
    initChart("mykfcChart", "$ Spend at all KFC by Month");

});

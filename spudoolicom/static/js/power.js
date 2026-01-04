function power() {
    fetch('/power')
        .then(response => response.text())
        .then(data => {
            document.getElementById('current_power').textContent = data;
        });
}

document.addEventListener('DOMContentLoaded', function () {
    setInterval(power, 6000);
});

function start() {
    power();
}

window.onload = start;

document.addEventListener('DOMContentLoaded', function () {
    // Helper function for benchleds
    function sendBenchLedsRequest(state) {
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/webcam/benchleds", true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send(JSON.stringify({
            onoroff: state
        }));
    }

    // Helper function for mancaveleds
    function sendMancaveLedsRequest(color) {
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/webcam/mancaveleds", true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send(JSON.stringify({
            mancaveleds: color
        }));
    }

    // Attach listeners for Bench LEDs
    const btnBenchOn = document.getElementById('btn-benchleds-on');
    if (btnBenchOn) {
        btnBenchOn.addEventListener('click', function () {
            sendBenchLedsRequest('on');
        });
    }

    const btnBenchOff = document.getElementById('btn-benchleds-off');
    if (btnBenchOff) {
        btnBenchOff.addEventListener('click', function () {
            sendBenchLedsRequest('off');
        });
    }

    // Attach listener for Mancave LEDs
    const btnMancave = document.getElementById('btn-mancaveleds');
    if (btnMancave) {
        btnMancave.addEventListener('click', function () {
            const colorInput = document.getElementById('mancaveledscolour');
            if (colorInput) {
                sendMancaveLedsRequest(colorInput.value);
            }
        });
    }
});

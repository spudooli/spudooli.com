document.addEventListener('DOMContentLoaded', function () {
    var mapElement = document.getElementById('map');
    if (!mapElement) return;

    var map = L.map('map').setView([-39, 175], 6);

    // Read markers data
    var dataElement = document.getElementById('map-data');
    if (dataElement) {
        try {
            var markers = JSON.parse(dataElement.textContent);
            markers.forEach(function (item) {
                // Ensure coords is an array. The template outputted something like [lat, lon] directly into JSON value position
                if (Array.isArray(item.coords)) {
                    L.marker(item.coords, { title: item.title, riseOnHover: true })
                        .bindPopup(`<a href="/photoblog/${item.id}" target="_blank" rel="noopener noreferrer">${item.title}</a>`)
                        .addTo(map);
                }
            });
        } catch (e) {
            console.error("Error parsing map data", e);
        }
    }

    // Style URL format in XYZ PNG format; see our documentation for more options
    L.tileLayer('https://tiles.stadiamaps.com/tiles/alidade_smooth/{z}/{x}/{y}{r}.png', {
        maxZoom: 20,
        attribution: '&copy; <a href="https://stadiamaps.com/" target="_blank">Stadia Maps</a>, &copy; <a href="https://openmaptiles.org/" target="_blank">OpenMapTiles</a> &copy; <a href="https://www.openstreetmap.org/copyright" target="_blank">OpenStreetMap</a>',
    }).addTo(map);
});

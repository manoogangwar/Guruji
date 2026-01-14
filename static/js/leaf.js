var map = L.map('map_div').setView([20, 0], 2);

// Add OpenStreetMap tiles
// L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
//     attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
// }).addTo(map);

L.tileLayer('http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}', {
	maxZoom: 40,
	subdomains: ['mt0', 'mt1', 'mt2', 'mt3'],
    attribution : 'Map data © <a href="https://maps.google.com">Google</a> contributors'
	}).addTo(map); 
// Initialize the marker variable
var redicon = L.icon({
    iconUrl: '/static/img/icons/locationmarker.png',
    iconSize: [80, 80]})


var marker = null;

// Function to update the location fields
function updateLocationFields(lat, lng) {
    document.getElementById('id_latitude').value = lat;
    document.getElementById('id_longitude').value = lng;
}

// const maxBounds = L.latLngBounds( L.latLng(6.4626999, 68.1097), 
// L.latLng(35.513327, 97.39535869999999) ); 
// this.map.setMaxBounds(maxBounds); this.map.fitBounds(maxBounds);

// Event listener for map click
map.on('click', function(e) {
    var lat = e.latlng.lat;
    var lon = e.latlng.lng;

    // Update the location fields
    updateLocationFields(lat, lon);

    // Add marker to the map
    if (marker) {
        map.removeLayer(marker);
    }
    marker = L.marker([lat, lon],{icon: redicon}).addTo(map);
});

// Add search control
var geocoder = L.Control.Geocoder.nominatim();
var searchControl = L.Control.geocoder({
    query: '',
    placeholder: 'Search for a location...',
    geocoder: geocoder
}).addTo(map);

// Event listener for search control
searchControl.on('markgeocode', function(e) {
    var lat = e.geocode.center.lat;
    var lon = e.geocode.center.lng;

    // Pan and zoom to the searched location without adding a marker
    map.setView([lat, lon], 13);

    // Update the location fields
    updateLocationFields(lat, lon);

    // Add marker to the map
    if (marker) {
        map.removeLayer(marker);
    }
    marker = L.marker([lat, lon],{icon: redicon}).addTo(map);
});
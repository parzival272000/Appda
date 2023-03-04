var locations = [
  [28.71474875494477, 75.5641488513994],
  [29.272094489297544, 77.05828932737279],
  [28.81105691052023, 77.49774240854144],
  [28.714748754944797, 76.9264534030222],
];
var map = L.map("map").setView([28.640753207620655, 77.24947873971865], 8);

const attribution =
  '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors';

const tileUrl = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";
const tiles = L.tileLayer(tileUrl, { attribution });
tiles.addTo(map);

L.marker([28.71474875494477, 75.5641488513994]).addTo(map); //Pilani

L.marker([29.272094489297544, 77.05828932737279]).addTo(map); //IFSAL Jindal
L.marker([28.81105691052023, 77.49774240854144]).addTo(map); //Jaypee greens
L.marker([28.714748754944797, 76.9264534030222]).addTo(map); //ICAT

map.on("click", function addMarker(e) {
  var newMarker = new L.marker(e.latlng).addTo(map);
  // console.log(e.latlng);
  let temp = [e.latlng.lat, e.latlng.lng];
  locations.push(temp);
  // console.log(locations);
});
var userLocBtn = document.getElementById("getUserLocation");
var userLocation;
userLocBtn.addEventListener("click", () => {
  navigator.geolocation.getCurrentPosition(correctLocation, errorLocation, {
    enableHighAccuracy: true,
  });
});

function correctLocation(position) {
  var newMarker = new L.marker([
    position.coords.latitude,
    position.coords.longitude,
  ]).addTo(map);
  userLocation = position;
  // findShortestDist(position);
  console.log(position);
}

function errorLocation(position) {
  console.log("can't get location");
}
var getNearestHelipadBtn = document.getElementById("getNearestHelipad");
getNearestHelipadBtn.addEventListener("click", () => {
  let minDist = Number.MAX_VALUE,
    idx;
  for (let i = 0; i < locations.length; i++) {
    let temp = getDistance(
      [userLocation.coords.latitude, userLocation.coords.longitude],
      [locations[i][0], locations[i][1]]
    );
    if (minDist > temp) {
      minDist = temp;
      idx = i;
    }
  }
  L.Routing.control({
    waypoints: [
      L.latLng(userLocation.coords.latitude, userLocation.coords.longitude),
      L.latLng(locations[idx][0], locations[idx][1]),
    ],
  }).addTo(map);
});

function getDistance(origin, destination) {
  var lon1 = toRadians(origin[1]),
    lat1 = toRadians(origin[0]),
    lon2 = toRadians(destination[1]),
    lat2 = toRadians(destination[0]);

  var deltaLat = lat2 - lat1;
  var deltaLon = lon2 - lon1;

  var a =
    Math.pow(Math.sin(deltaLat / 2), 2) +
    Math.cos(lat1) * Math.cos(lat2) * Math.pow(Math.sin(deltaLon / 2), 2);
  var c = 2 * Math.asin(Math.sqrt(a));
  var EARTH_RADIUS = 6371;
  return c * EARTH_RADIUS * 1000;
  // return L.CRS.distance(from, to).toFixed(0)/1000;
}

function toRadians(n) {
  return (n * Math.PI) / 180;
}

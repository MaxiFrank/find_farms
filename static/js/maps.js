"use strict";

function moveToLocation(lat, lng, zoom){
  const center = new google.maps.LatLng(lat, lng);

  window.map.panTo(center);
  map.setZoom(zoom)
  }

function addBookMark(results) {
  alert('farm has been added');
  const lat = window.marker.position.lat();
  const lng = window.marker.position.lng();
  window.marker.setMap(null);
  const marker = new google.maps.Marker({
    position: new google.maps.LatLng(lat, lng),
    title: 'stuff',
    map: window.map,
    optimized: true, 
    icon: {  // custom icon
      url: '/static/img/marker.svg',
      scaledSize: {
        width: 30,
        height: 30
      }
    }
  });


  marker.addListener('click', (event) => {
  console.log(marker);

  });

const infoWindow = new google.maps.InfoWindow({
                              content: markerInfo,
                              maxWidth: 200});
                        
marker.addListener('click', (event) => {
  infoWindow.open(window.map, marker);
  console.log(marker)
});
}

function addFarm() {
  const currentLink = document.querySelector('#current-link').getAttribute('href')
  const data = {'current-link':currentLink}
  $.post("/api/bookmark", data, addBookMark, 'json');

}

function makeMarker(centerLon, centerLat, lon, lat, link, zoom) {
  moveToLocation(centerLon, centerLat, zoom)
  const marker = new google.maps.Marker({
                              position: new google.maps.LatLng(lat, lon),
                              title: 'stuff',
                              link: link, 
                              map: window.map,
                              optimized: true, 
                              icon: {  // custom icon
                                url: 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
                                // url: '/static/img/marker.svg',
                                scaledSize: {
                                  width: 30,
                                  height: 30
                                }
                              }
                            });                
  const markerInfo = (`
    <h1>${marker.title}</h1>
        <p>
          Located at: <code>${marker.position.lat()}</code>,
          <code>${marker.position.lng()}</code>
          <code><a target='_blank' id='current-link' href='${marker.link}'>click here</a></code>
          <code><div id="bookmark_farm_button" method="POST">Add to bookmark <button onclick="addFarm()">Add please!</button></div></code>
        </p>`);

  const infoWindow = new google.maps.InfoWindow({
                                content: markerInfo,
                                maxWidth: 200});
                          
  marker.addListener('click', (event) => {
    infoWindow.open(window.map, marker);
    console.log(marker)
    window.marker = marker
  });



  return marker
};


function fetchFavorites() {
  fetch('/api/bookmarked')
  .then(function(response) {
    response.json()
  .then(function(data) {
    for (let i=0; i<data.length; i++) {
      makeMarker(data[i].center_lat, data[i].center_lon, data[i].lon, data[i].lat, data[i].link, data[i].zoom);
    }
  })
})
}


  $("#bookmark_farm_button").on('submit', addFarm);

function initMap() {
  const initCoords = {
    lat: 39.8283,
    lng: -98.5795
  };

  const basicMap = new google.maps.Map(
    document.querySelector('#map'),
    {
      center: initCoords,
      zoom: 4
    }
  );
  
  window.map = basicMap

  fetchFavorites()
}
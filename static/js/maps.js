"use strict";

function moveToLocation(lat, lng, zoom){
  const center = new google.maps.LatLng(lat, lng);

  window.map.panTo(center);
  map.setZoom(zoom)
  }

function addBookMark(results) {
  const lat = window.marker.position.lat();
  const lng = window.marker.position.lng();
  const title = window.marker.getTitle()
  const link = window.marker.link
  window.marker.setMap(null);
  const marker = new google.maps.Marker({
    position: new google.maps.LatLng(lat, lng),
    title: title,
    map: window.map,
    optimized: true, 
    icon: {
      url: '/static/img/cow.svg',
      scaledSize: {
        width: 30,
        height: 30
      }
    }
  });

  const markerInfo = (`
  <div id='current-title'>'${title}'</div>
      <p>
        <code><a target='_blank' id='current-link' href='${link}'>see more details here</a></code>
      </p>`);

  const infoWindow = new google.maps.InfoWindow({
                              content: markerInfo,
                              maxWidth: 200});
                        
  marker.addListener('click', (event) => {
    infoWindow.open(window.map, marker);
});
}

function addFarm() {
  const currentLink = document.querySelector('#current-link').getAttribute('href')
  const currentTitle = document.querySelector('#current-title').innerText
  const data = {'current-link':currentLink
                ,'current-title':currentTitle}

  $.post("/api/bookmark", data, addBookMark, 'json');

}

function makeMarker(centerLon, centerLat, lon, lat, link, zoom, title, icon_link) {
  moveToLocation(centerLon, centerLat, zoom)
  const marker = new google.maps.Marker({
                              position: new google.maps.LatLng(lat, lon),
                              title: title,
                              link: link, 
                              map: window.map,
                              optimized: true, 
                              icon: {
                                url: icon_link,
                                scaledSize: {
                                  width: 30,
                                  height: 30
                                }
                              }
                            });              

  const markerInfo = (`
    <div id='current-title'>'${marker.title}'</div>
        <p>
          <code><a target='_blank' id='current-link' href='${marker.link}'>see more details here</a></code>
          <code><div class="bookmark_farm_button" method="POST"><button onclick="addFarm()">Add to Favorites</button></div></code>
        </p>`);

  const infoWindow = new google.maps.InfoWindow({
                                content: markerInfo,
                                maxWidth: 200});
                          
  marker.addListener('click', (event) => {
    infoWindow.open(window.map, marker);
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
      makeMarker(data[i].center_lat, data[i].center_lon, data[i].lon, data[i].lat, data[i].link, data[i].zoom, data[i].title,'/static/img/cow.svg');
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
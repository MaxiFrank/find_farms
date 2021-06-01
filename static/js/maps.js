"use strict";

// We use a function declaration for initMap because we actually *do* need
// to rely on value-hoisting in this circumstance.

// .get issues http request to whichever server served up the request.
// broswer sends a request, if you get a response, calls showFortune and pass response in as an argument to newFortune.

// need to figure out how to get the list of farms that fit all my criteria here


// set up a function to receive data?
  // Maybe inplement this later
function moveToLocation(lat, lng, zoom){
  const center = new google.maps.LatLng(lat, lng);
  // using global variable:
  window.map.panTo(center);
  map.setZoom(zoom)
  }
// moveToLocation(37.8044, -122.2712)

function makeMarker(centerLon, centerLat, lon, lat, link, zoom) {
  moveToLocation(centerLon, centerLat, zoom)
  
  // const marker_obj = {'name':'Farm 1',
  //                 'coords': {'lat':lat,
  //                           'lon':lon
  //                           }
  //                 };
                  
  const marker = new google.maps.Marker({
                              position: new google.maps.LatLng(lat, lon),
                              // title: 'stuff',
                              map: window.map
                              // icon: {  // custom icon
                              //   url: '/static/img/marker.svg',
                              //   scaledSize: {
                              //     width: 30,
                              //     height: 30
                              //   }
                              // }
                            });
  marker.addListener('click', (event) => {
    // why is this not giving my tabs that would stay in the brower?
    window.open(link, '_blank_')
    // const result = document.querySelector('.result');
    // result.textContent = `Add ${link} to bookmark?`
  });

  return marker
};

  // upon clicking on the marker, go to the farm page



function initMap() {
  // the center of my map upon display (so this should be the either the state or the zip code I entered)
  const initCoords = {
    lat: 39.8283,
    lng: -98.5795
  };

  const basicMap = new google.maps.Map(
    document.querySelector('#map'),
    {
      center: initCoords,
      // 0 is the whole world, 20/21 is the highest zoom
      zoom: 4
    }
  );
  
  window.map = basicMap
  

  // this is where the farms go (need to look at documentation and stackoverflow basically)
  // const sfMarker = new google.maps.Marker({
  //   position: sfBayCoords, // need to update this one.... basically a loop. what to do if I want to have multiple
  //   title: 'SF Bay', // this is the tooltip. might want farm info to display here
  //   map: basicMap // the map I am using to render all my points.
  // });


  // provide context for aspect of the map
  // const sfInfo = new google.maps.InfoWindow({
  //   content: '<h1>Montana!</h1>' // can include images here (how terrible would it be to include a picture of the farm here...)
  // });

  // sfInfo.open(basicMap, sfMarker);

  // want farms here
  // const locations = [
  //   {
  //     name: 'Farm 1',
  //     coords: {
  //       lat: 47.1625441,
  //       lng: -114.0847398 
  //     }
  //   },
  //   {
  //     name: 'Farm 2',
  //     coords: {
  //       lat:  46.0215872,
  //       lng: -114.1731427
  //     }
  //   }
  // ];

  // create markers with custom icons
  // const markers = [];
  // for (const location of locations) {
  //   markers.push(new google.maps.Marker({
  //     position: location.coords,
  //     title: location.name,
  //     map: basicMap,
  //     icon: {  // custom icon
  //       url: '/static/img/marker.svg',
  //       scaledSize: {
  //         width: 30,
  //         height: 30
  //       }
  //     }
  //   }));
  // }

  // for (const marker of markers) {
  //   const markerInfo = (`
  //     <h1>${marker.title}</h1>
  //     <p>
  //       Located at: <code>${marker.position.lat()}</code>,
  //       <code>${marker.position.lng()}</code>
  //     </p>
  //   `);

  //   const infoWindow = new google.maps.InfoWindow({
  //     content: markerInfo,
  //     maxWidth: 200
  //   });

  //   marker.addListener('click', () => {
  //     infoWindow.open(basicMap, marker);
  //   });
  // }
}

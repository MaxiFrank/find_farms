var currentState = ''
function captureValue(objButton) {
  currentState = objButton.innerText;
  console.log('click state')
  console.log(currentState);
}

function updateFarms(results) {
  centerLon = results[0]
  centerLat = results[1]

  if (results[3] < 50) {
    zoom = 10;
  } else if (results[3] > 50) {
    zoom = 8;
  } else {
    zoom = 9
  }
  for (i = 0; i < results[2].length; i++) {
    makeMarker(centerLat, centerLon, results[2][i].lon, results[2][i].lat, results[2][i].link, zoom, results[2][i].title, 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png');
  }
}

function showFarms(evt) {
  console.log('show farm state')
  console.log(currentState);
  evt.preventDefault();

  if (!document.querySelector('#zip_code_field')) {
    console.log('no zip code')
    var zip_code = undefined; 
  } else {
    var zip_code = document.querySelector('#zip_code_field').value;
  }
    
  if (!document.querySelector('#miles_field')){
    console.log('no miles')
    var miles = undefined; 
  } else {
    var miles = document.querySelector('#miles_field').value;
  }

  let state = window.currentState;
  let months = document.querySelector('#months_field');
  const selectedList = [];
  for (let option of months.options) {
    if (option.selected) {
      selectedList.push(option.value);
    }
  }
  const data = {
    'zip_code': zip_code
    , 'miles': miles
    , 'state': state
    , 'months': selectedList
  }
  $.post("/api/farms", data, updateFarms, 'json');
}

$("#additonal-location-form").on('submit', showFarms);


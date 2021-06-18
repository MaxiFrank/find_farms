var currentState = ''
function captureValue(objButton){  
  currentState =  objButton.innerText;
  console.log(currentState);
}

function updateFarms(results) {
    centerLon = results[0]
    centerLat = results[1]  
    
    if (results[3] < 50){
      zoom = 10;
    } else if  (results[3] > 50) {
      zoom = 8;
    } else {
      zoom = 9
    }
    for (i=0; i<results[2].length; i++){
      makeMarker(centerLat, centerLon, results[2][i].lon, results[2][i].lat, results[2][i].link, zoom, results[2][i].title);
    }
  }

  function showFarms(evt) {
    console.log(currentState);
    evt.preventDefault();
    let zip_code = document.querySelector('#zip_code_field').value;
    let miles = document.querySelector('#miles_field').value;
    let state = window.currentState
    let months = document.querySelector('#months_field');
    const selectedList = [];
    for (let option of months.options) {
      if (option.selected) {
        selectedList.push(option.value)
      }
    }
    
    const data = {'zip_code':zip_code
                , 'miles':miles
                , 'state':state
                , 'months':selectedList}
    $.post("/api/farms", data, updateFarms, 'json');
  }

  $("#additonal-location-form").on('submit', showFarms);


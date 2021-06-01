function updateFarms(results) {
    // console.log('updatedFarms')
    // console.log(results)
    centerLon = results[0]
    centerLat = results[1]  
    
    if (results[3] < 50){
      zoom = 10;
    } else {
      zoom = 8;
    }

    for (i=0; i<results[2].length; i++){
      // console.log(results[i]);
      makeMarker(centerLat, centerLon, results[2][i].lon, results[2][i].lat, results[2][i].link, zoom);
    }

    // $('#farm-text').html(results);
  }

  // need to make a marker for all the farms that come up in results, so need to iterate through results.
  function showFarms(evt) {
    evt.preventDefault();
    let zip_code = document.querySelector('#zip_code_field').value;
    let miles = document.querySelector('#miles_field').value;
    let months = document.querySelector('#months_field');
    const selectedList = [];
    for (let option of months.options) {
      if (option.selected) {
        selectedList.push(option.value)
      }
    }
    console.log(months);
    // console.log(selectedList.value)
    console.log(selectedList)
    

    // data here isn't what I want to send to api/farms, I think I need to figure out what the data being sent is
    const data = {'zip_code':zip_code
                , 'miles':miles
                , 'months':selectedList}
    // console.log(data)
    // params = {zip_code:zip_code, miles:miles};
    $.post("/api/farms", data, updateFarms, 'json');
    // $.get("/api/farms", params, updateFarms);
  }
  
  // console.log($("#additonal-location-form"));
  // I am not calling showFarms correctly. when I call it in the browser, it loads.
  $("#additonal-location-form").on('submit', showFarms);


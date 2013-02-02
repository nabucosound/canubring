function google_places_autocomplete_widget() {
  var options = {
    types: ['(cities)'],
  };
  $('.city-input').each(function() {
    autocomplete = new google.maps.places.Autocomplete(this, options);
  });
  $(function() {
    $(".datepicker").each(function() {
      $(this).datepicker({ minDate: 0 });
    })
  });
}

$(document).ready(function(){
  google_places_autocomplete_widget();
})


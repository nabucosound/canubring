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

  $('#new-trip-submit-btn').click(function() {
    var data = new Array()
    $('form#new-trip-form').each(function() {
      data.push($(this).serializeFormJSON());
    })
    $.ajax({
      url: '/api/v1/trip/',
      type: 'patch',
      dataType: 'application/json',
      contentType: 'application/json',
      data: '{"objects": '+JSON.stringify(data)+'}',
      complete: function(xhr, textStatus) {
          //console.log(xhr.status);
          window.location = "/my/trips/";
      }
    });
  });

  $('#manage-legs-container').on(
    {
      click: function loadTripLeg (e) {
        $.get('/my/triplegform/', function(data) {
          $('#trip-legs-container').append(data);
          google_places_autocomplete_widget();
        });
        $('.remove-leg').show();
        return false;
      }
    },
    '.add-leg'
  );

  $('#manage-legs-container').on(
    {
      click: function removeTripLeg (e) {
        $('#trip-legs-container').find('.item-leg:last').remove();
        itemlegs = $('#trip-legs-container').find('.item-leg');
        if (itemlegs.length == 1) {
          $(this).hide();
        }
        return false;
      }
    },
    '.remove-leg'
  );

})


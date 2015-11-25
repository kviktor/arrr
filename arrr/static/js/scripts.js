/* Project specific Javascript goes here. */

function sideNav() {
  if ($(window).width() < 769) {
    $('.off-canvas-wrap').removeClass('move-right');
    $('.left-off-canvas-toggle').show();
  } else {
    $('.off-canvas-wrap').addClass('move-right');
    $('.left-off-canvas-toggle').hide();
  }
}



$(window).resize(function() {
  sideNav();
});


$(function() {
  // yesterday
  var now = (new Date()).setDate((new Date()).getDate() - 1);
  $(".datetimeinput").fdatepicker({
    'language': 'hu',
    'format': "yyyy-mm-dd hh:ii",
    'pickTime': true,
    'onRender': function (date) {
      return date.valueOf() < now.valueOf() ? 'disabled' : '';
    }
  });
});


$(function() {

  if($("#calendar").length) { 
    $.ajax({
      url: "/data/calendar.json",
      success: function(data) {
        initCalendar(data.rooms, data.reservations);
      }
    });
  }

  function initCalendar(rooms, events) {
    $("#calendar").fullCalendar({
      schedulerLicenseKey: 'GPL-My-Project-Is-Open-Source',
      header: {
        left: 'prev,next today',
        center: 'title',
        right: 'timelineDay,agendaWeek,month'
      },
      height: "auto",
      lang: "en",
      defaultView: 'timelineDay',
      fixedWeekCount: false,
      allDaySlot: false,
      resourceLabelText: 'Rooms',
      minTime: "07:00:00",
      maxTime: "21:00:00",
      resources: rooms,
      events: events

    });
    $("#calendar button").prop("class", "").prop("disabled", false);
  }
});

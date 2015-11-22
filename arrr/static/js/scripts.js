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

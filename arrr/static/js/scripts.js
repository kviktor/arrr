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

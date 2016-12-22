function resizeText(multiplier) {
  var html = document.getElementsByTagName('html')[0];
  if (html.style.zoom == "") {
    html.style.zoom = "1";
  }
  html.style.zoom = parseFloat(html.style.zoom) + (multiplier * 0.1);
  setCookie('textSize', html.style.zoom);
}

// Resize Text on page load using cookie value
$('html').css('zoom', getCookie('textSize'));
$('#plustext').bind('click', function(){resizeText(1);});
$('#minustext').bind('click', function(){resizeText(-1);});
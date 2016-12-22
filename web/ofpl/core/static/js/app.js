$(document).foundation({

});

function setCookie(c_name,value,exdays)
  {
  var exdate=new Date();
  exdate.setDate(exdate.getDate() + exdays);
  var c_value=escape(value) + 
  ((exdays==null) ? "" : ("; expires="+exdate.toUTCString()));
  document.cookie=c_name + "=" + c_value;
  }

function getCookie(c_name)
  {
  var i,x,y,ARRcookies=document.cookie.split(";");
  for (i=0;i<ARRcookies.length;i++)
    {
    x=ARRcookies[i].substr(0,ARRcookies[i].indexOf("="));
    y=ARRcookies[i].substr(ARRcookies[i].indexOf("=")+1);
    x=x.replace(/^\s+|\s+$/g,"");
    if (x==c_name)
      {
      return unescape(y);
      }
    }
  }

function resizeText(multiplier) {
  var html = document.getElementsByTagName('html')[0];
  if (html.style.zoom == "") {
    html.style.zoom = "1";
  }
  html.style.zoom = parseFloat(html.style.zoom) + (multiplier * 0.1);
  setCookie('textSize', html.style.zoom);
}

// Resize Text on page load using cookie value
var html = document.getElementsByTagName('html')[0];
html.style.zoom = getCookie('textSize');
var equalize_height = function(){
  var maxHeight = (function(){
    var max = $('table.calendar-grid td').width()/2; // at least half a square
    $('table.calendar-grid td .event-list').each(function(index, element){
      var $elm = $(element);
      console.log($elm);
      var height = $elm.height();
      if(height > max){
        max = height;
      }
    });

    return max;
  })();

  $('table.calendar-grid td .event-list').css('height', maxHeight + 'px');
}


setTimeout(function(){
  equalize_height();
}, 500);

$(window).on('resize', equalize_height);

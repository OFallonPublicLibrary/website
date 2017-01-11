var equalize_height = function(){
  var maxHeight = (function(){
    var max = 0;
    $('table.calendar-grid td').each(function(index, element){
      var $elm = $(element);
      console.log($elm);
      var height = $elm.height();
      if(height > max){
        max = height;
      }
    });

    return max;
  })();

  $('table.calendar-grid td').css('height', maxHeight + 'px');
}


setTimeout(function(){
  equalize_height();
}, 500);

$(window).on('resize', equalize_height);

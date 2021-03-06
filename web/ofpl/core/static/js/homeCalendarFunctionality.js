function nth(d) {
  if(d>3 && d<21) return 'th';
  switch (d % 10) {
        case 1:  return "st";
        case 2:  return "nd";
        case 3:  return "rd";
        default: return "th";
    }
}

function getShortMonth(month)   {
        switch(month)   {
                case 0: return 'Jan';
                case 1: return 'Feb';
                case 2: return 'Mar';
                case 3: return 'Apr';
                case 4: return 'May';
                case 5: return 'Jun';
                case 6: return 'Jul';
                case 7: return 'Aug';
                case 8: return 'Sep';
                case 9: return 'Oct';
                case 10: return 'Nov';
                case 11: return 'Dec';
                default: return false;
        }
}

function highlightCells(year, month){
    $.getJSON("/dateJSON/" + year + "-" + (month + 1) + ".json", function( data ){
          $(".ui-state-default").each(function(){
            var test = $(this).html();
            if(data.days.indexOf(test.toString()) > -1){
              $(this).addClass("nonEmpty");
            }
          });
    });
}

function showDaysEvents(date){
    var currentDate = $( " #datepicker " ).datepicker( "getDate" );
    var day = currentDate.getDate();
    var month = currentDate.getMonth()+1;
    var year = currentDate.getFullYear();
    $('#eventDate').html(getShortMonth(month-1) + " " + day + nth(day));
    $('#eventContainer').html("<img src=\"/static/images/ajax-loader.gif\"><br><em>Loading...</em>");
    $('#eventContainer').load("/date/" + year + "-"  + month + "-"  + day + ".html");
    highlightCells(currentDate.getFullYear(), currentDate.getMonth());
}

$( "#datepicker" ).datepicker({
    inline: true,
    onSelect: function(date){
        $(".ui-datepicker a").removeAttr("href");
        showDaysEvents(date);
    },
    onChangeMonthYear: function(year, month, inst){
        highlightCells(year, month - 1);
    }
});

var rightNow = new Date();

// set event for today and highlight the months
showDaysEvents(rightNow);

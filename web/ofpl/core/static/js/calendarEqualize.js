if ($(".calDate-0")[0]) { // If the class is present on the page

var equalizeCalendarRows = function(classname){
    $(classname).height("auto");
    var maxHeight = 0;
    $(classname).each(function(){
       if ($(this).height() > maxHeight) { maxHeight = $(this).height(); }
    });
    $(classname).height(maxHeight + 10);
}

function eqAll(){
    equalizeCalendarRows(".calDate-0");
    equalizeCalendarRows(".calDate-1");
    equalizeCalendarRows(".calDate-2");
    equalizeCalendarRows(".calDate-3");
    equalizeCalendarRows(".calDate-4");
    equalizeCalendarRows(".calDate-5");
}

$( window ).resize(function() {
    setTimeout(function(){
        eqAll();
    }, 50);
});

eqAll();

};
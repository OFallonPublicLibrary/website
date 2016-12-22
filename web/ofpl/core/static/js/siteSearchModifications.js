if ($('html').hasClass('isSiteSearchPage')) {


// get rid of ugly heading
$('.search-headline').remove();

// get rid of random table divider
$('.search-line').remove();
$('.search-header-table').remove();

// store things from elements we are about to delete and remake better
var searchTerms = $("input[name='query']")[0].value;
var nextPreviousLinksHtml = $(".search-nav").eq(0).contents();

// remove search nav boxes
$('.search-nav-form-table').remove()



// replace <font> tags with <div>'s
while(0 < $('font.search-results').size()){

	var innerHTML = $('font.search-results').eq(0).contents();

    $('font.search-results').eq(0).replaceWith(
    	$('<div></div>').addClass('search-result').append(
    		$('<p></p>').append(innerHTML)
    	)
    );

}



// add search terms into search box after a short delay
window.setTimeout(function(){
    $('#searchBoxInput').click();                   // open the dropdown
    $("input[name='searchOptions']").eq(2).click(); // change form target to site search
    $("#searchBoxInput").val(searchTerms);          // put search terms into the box
    $("form.srchbx_wrapper").trigger("mouseout");   // close the dropdown
}, 1000);

// add search terms into search box after a short delay
window.setTimeout(function(){
    $('#searchBoxInput').click();                   // open the dropdown
    $("input[name='searchOptions']").eq(2).click(); // change form target to site search
    $("#searchBoxInput").val(searchTerms);          // put search terms into the box
    $("form.srchbx_wrapper").trigger("mouseout");   // close the dropdown
}, 3000);


// add next and previous links back into the page
nextPrevious2 = nextPreviousLinksHtml.clone();

$('<div></div>').addClass('nextPreviousLinks').append(nextPreviousLinksHtml).insertAfter($('.search-results'));
$('<div></div>').addClass('nextPreviousLinks').append(nextPrevious2).insertBefore($('.search-results'));



}; // end if
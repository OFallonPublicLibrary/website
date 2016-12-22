$(document).ready(function(){
	var addMainCarousel = function(){
		$('.main-carousel').slick({
	  		infinite: true,
	  		dots: true,
	  		arrows: false,
	  		touchThreshold: 5,
        	autoplay: true,
        	autoplaySpeed: 8000,
        	lazyLoad: 'progressive'
		});
	}
	var equalizeSlideCaptions = function(){
		$(".slideCaption").height("auto");
		var maxHeight = 0;
		$(".slideCaption").each(function(){
		   if ($(this).height() > maxHeight) { maxHeight = $(this).height(); }
		});
		$(".slideCaption").height(maxHeight);
	}

	$( window ).resize(function() {
		setTimeout(function(){
			equalizeSlideCaptions();
		}, 50);
	});

	var initializeSlider = function(){
		addMainCarousel();
		equalizeSlideCaptions();
	}

	var reinitializeSlider = function(){
		$('.main-carousel').unslick();
		initializeSlider();
	}


	window.setTimeout(function(){
		initializeSlider();
	}, 100);
	// Delay slider initialization so Foundation's (hacked) interchange can swap out the 'data-lazy' attribute's value

});

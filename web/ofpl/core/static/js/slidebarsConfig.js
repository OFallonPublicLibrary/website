(function($) {
				$(document).ready(function() {
					// Initiate Slidebars
					var mySlidebars = new $.slidebars();
					
					// Slidebars Submenus
					$('.sb-toggle-submenu').off('click').on('click', function() {
						$submenu = $(this).parent().children('.sb-submenu');
						$(this).add($submenu).toggleClass('sb-submenu-active'); // Toggle active class.
						
						if ($submenu.hasClass('sb-submenu-active')) {
							$submenu.slideDown(200);
						} else {
							$submenu.slideUp(200);
						}
					});
				});
			}) (jQuery);
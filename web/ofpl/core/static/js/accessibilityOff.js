            // This enables the accessibility highlighting if a person presses the tab key (13)
            $('a, #button-text, #button-hamburger').bind('keyup', function(e){
                if (e.which == 9) {
                    $('body').removeClass('nofocushighlight');
                }
                return false;
            })

            // This overwrites the focus styles if a link is hit with a mouse

            $('a, #button-text, #button-hamburger').bind('mouseup keyup', function(e){
                if (e.which == 1) {
                    $('body').addClass('nofocushighlight');
                }
                return false;
            })

            // This overwrites the focus styles if a link is hit with a mouse
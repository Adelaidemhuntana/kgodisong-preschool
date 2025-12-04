(function ($) {
    "use strict";
    
    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });


    $(".btn-toggle-nav a").click(function() {  
        $(".btn-toggle-nav a").removeClass("active");
        $(this).addClass("active");  
    });

    
})(jQuery);


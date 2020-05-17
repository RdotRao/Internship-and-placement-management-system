jQuery(function($) {
    var path = window.location.href;
    $('a').each(function() {
        if (this.href === path) {
            $(this).addClass('active');
        }
    });
});
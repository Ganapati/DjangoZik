$(document).ready(function(){

    // Initial redirection if direct url to content
    var dst = window.location.hash;
    if (dst.length > 0) {
        redirect(dst.substring(1));
    }

    // Ajaxify links
    $(document).on('click', 'a.async', function() {
        var dst = $(this).attr("href");
        window.location.hash = '#' + dst;
        return false;
    });

    // Handle
    $(window).on('hashchange', function() {
        var dst = window.location.hash.substring(1);
        redirect(dst);
    });

    // Change menu button style
    $(document).on('click', 'ul.nav-sidebar li a', function() {
        $("li.active").removeClass("active");
        $(this).closest("li").addClass("active");
    });

});

// Url handler
function redirect(dst) {
    success_box("Loading :", dst);
    $.get(dst, function(data){
        $("#site_content").html(data);
        $(".alert.alert-success").hide();
    });
}

function set_active_tab(name) {
    $("li.active").removeClass("active");
    $(name).addClass("active");
}

$(document).ready(function(){

    // Initial redirection if direct url to content
    var dst = window.location.hash;
    if (dst.length > 0) {
        redirect(dst.substring(1));
    }


    // Search
    $("#search_input").keydown(function(e){
        var key = e.charCode ? e.charCode : e.keyCode ? e.keyCode : 0;
        if (key == 13) {
            keyword = encodeURIComponent($("#search_input").val());
            success_box("Searching :", $("#search_input").val());
            $.get('/search/' + keyword, function(data){
                $("#site_content").html(data);
                $(".alert.alert-success").hide();
            });
            return false;
        }
    });
});

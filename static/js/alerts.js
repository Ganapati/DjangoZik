$(document).ready(function(){

    // Hide alert boxes on load
    $(".alert").hide();

    // Handle warning close button
    $(".alert-warning .close").click(function(){
        $(".alert.alert-warning").hide();
    });
    
    // Handle success close button
    $(".alert-success .close").click(function(){
        $(".alert.alert-success").hide();
    });

});

// Warning boxes
function alert_box(title, text) {
    $(".alert-warning .alert_title").html(title);
    $(".alert-warning .alert_text").html(text);
    $(".alert.alert-warning").show();
    $('html, body').animate({scrollTop:0}, 500);
}

// Success box
function success_box(title, text) {
    $(".alert-success .alert_title").html(title);
    $(".alert-success .alert_text").html(text);
    $(".alert.alert-success").show();
    $('html, body').animate({scrollTop:0}, 500);
}

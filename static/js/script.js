$(document).ready(function(){

    song_to_playlist = "";
    $(".alert").hide();

    $("#jquery_jplayer_1").jPlayer({
        ready: function () {
          $(this).jPlayer();
        },
        swfPath: "/static/Jplayer/",
        supplied: "mp3"
      });

    $("#jquery_jplayer_1").bind($.jPlayer.event.ended, function() {
        var playing = $(".info");
        $(".info").removeClass("info");
        if (playing.next().is("tr")) {
            var next = playing.next();
            var next_song = next.find("a:first");
            next.addClass("info");
            $(this).jPlayer("setMedia", {
                title: next_song.html(),
                mp3: next_song.attr("data-source")
            });
            $(this).jPlayer("play");
        }
    });

    // Handle Song click
    $(document).on('click', '.song', function() {
        var filepath = $(this).attr('data-source');
        $("tr").removeClass("info");
        $(this).closest("tr").addClass("info");
        var self = $(this);
        $("#jquery_jplayer_1").jPlayer("setMedia", {
            title: self.html(),
            mp3: filepath
        });
        $("#jquery_jplayer_1").jPlayer("play");
        return false;
    });

    // Handle Radio click
    $(document).on('click', '.play_radio', function() {
        var url = $(this).attr('data-url');
        $("tr").removeClass("info");
        $(this).closest("tr").addClass("info");
        var self = $(this);
        $("#jquery_jplayer_1").jPlayer("setMedia", {
            title: self.html(),
            mp3: url
        });
        $("#jquery_jplayer_1").jPlayer("play");
        return false;
    });

    // Add Radio
    $(document).on('click', '#add_radio', function() {
        var self = $(this);
        var radio_url = $("#radio_name").val();
        $.get("/ajax/add_radio/" + Base64.encode(radio_url), function(data){
            if (data.success) {
                $(".table_radio tr:last").after('<tr> \
                        <td> \
                            <a href="#" class="play_radio" class="btn_radio" data-url="' + data.message['url'] + '">' + data.message['url'] + '</a> \
                        </td> \
                        <td> \
                            <a href="" class="delete_radio" data-id="' + data.message['id'] + '"> \
                                <span class="glyphicon glyphicon-minus-sign"></span> \
                            </a> \
                        </td> \
                    </tr>');
                success_box("Yay !", "Radio added.");
            } else {
                alert_box("Oops !", "Error adding radio.");
            }
        });
        return false;
    });

    // Delete radio
    $(document).on('click', '.delete_radio', function() {
        var radio = $(this).data("id");
        var self = $(this);
        $.get("/ajax/delete_radio/" + radio, function(data){
            if (data.success) {
                self.closest("tr").remove();
                success_box("Yay !", "Radio deleted.");
            } else {
                alert_box("Oops !", "Error deleting radio.");
            }
        });
        return false;
    });

    // Add Playlist
    $(document).on('click', '#add_playlist', function() {
        var self = $(this);
        var playlist_url = $("#playlist_name").val();
        $.get("/ajax/add_playlist/" + playlist_url, function(data){
            if (data.success) {
                $(".table_playlist tr:last").after('<tr> \
                        <td> \
                            <a class="async" href="/songs/playlist/' + data.message['slug'] + '">' + data.message['name'] + '</a></li> \
                        </td> \
                        <td> \
                            <a href="" class="delete_playlist" data-slug="' + data.message['slug'] + '"> \
                                <span class="glyphicon glyphicon-minus-sign"></span> \
                            </a> \
                        </td> \
                    </tr>');
                success_box("Yay !", "Playlist added.");
            } else {
                alert_box("Oops !", "Error adding playlist.");
            }
        });
        return false;
    });

    // Delete playlist
    $(document).on('click', '.delete_playlist', function() {
        var playlist = $(this).data("slug");
        var self = $(this);
        $.get("/ajax/delete_playlist/" + playlist, function(data){
            if (data.success) {
                self.closest("tr").remove();
                success_box("Yay !", "Playlist deleted.");
            } else {
                alert_box("Oops !", "Error deleting playlist.");
            }
        });
        return false;
    });

    // Remove song from playlist
    $(document).on('click', '.remove_from_playlist', function() {
        var playlist = $(this).data("playlist");
        var song = $(this).data("slug");
        var self = $(this);
        $.get("/ajax/remove_song_from_playlist/" + song + "::" + playlist, function(data){
            if (data.success) {
                self.closest("tr").remove();
                success_box("Yay !", "Song removed from playlist.");
            } else {
                alert_box("Oops !", "Error removing song from playlist.");
            }
        });
        return false;
    });

    // Modal playlist
    $(document).on('click', '.add_to_playlist', function() {
        var nb_playlists = $("option.playlist");
        if (nb_playlists.length > 0) {
            song_to_playlist = $(this).data("slug");
            $('#modal_playlist').modal({show:true})
        } else {
            alert_box("Oops !", "No playlist available.");
        }
        return false;
    });

    // Add a song to playlist
    $(document).on('click', '.btn.add_song_to_playlist', function() {
        $.get( "/ajax/playlist/" + $("#modal_playlist select").val() + "::" + song_to_playlist, function( data ) {
            if (data.success) {
                success_box("Yay !", "Song added to playlist.");
            } else {
                alert_box("Oops !", "Error adding song to playlist.");
            }
        });
        $('#modal_playlist').modal('hide');
    });

    // Base64
    var Base64={_keyStr:"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",encode:function(e){var t="";var n,r,i,s,o,u,a;var f=0;e=Base64._utf8_encode(e);while(f<e.length){n=e.charCodeAt(f++);r=e.charCodeAt(f++);i=e.charCodeAt(f++);s=n>>2;o=(n&3)<<4|r>>4;u=(r&15)<<2|i>>6;a=i&63;if(isNaN(r)){u=a=64}else if(isNaN(i)){a=64}t=t+this._keyStr.charAt(s)+this._keyStr.charAt(o)+this._keyStr.charAt(u)+this._keyStr.charAt(a)}return t},decode:function(e){var t="";var n,r,i;var s,o,u,a;var f=0;e=e.replace(/[^A-Za-z0-9\+\/\=]/g,"");while(f<e.length){s=this._keyStr.indexOf(e.charAt(f++));o=this._keyStr.indexOf(e.charAt(f++));u=this._keyStr.indexOf(e.charAt(f++));a=this._keyStr.indexOf(e.charAt(f++));n=s<<2|o>>4;r=(o&15)<<4|u>>2;i=(u&3)<<6|a;t=t+String.fromCharCode(n);if(u!=64){t=t+String.fromCharCode(r)}if(a!=64){t=t+String.fromCharCode(i)}}t=Base64._utf8_decode(t);return t},_utf8_encode:function(e){e=e.replace(/\r\n/g,"\n");var t="";for(var n=0;n<e.length;n++){var r=e.charCodeAt(n);if(r<128){t+=String.fromCharCode(r)}else if(r>127&&r<2048){t+=String.fromCharCode(r>>6|192);t+=String.fromCharCode(r&63|128)}else{t+=String.fromCharCode(r>>12|224);t+=String.fromCharCode(r>>6&63|128);t+=String.fromCharCode(r&63|128)}}return t},_utf8_decode:function(e){var t="";var n=0;var r=c1=c2=0;while(n<e.length){r=e.charCodeAt(n);if(r<128){t+=String.fromCharCode(r);n++}else if(r>191&&r<224){c2=e.charCodeAt(n+1);t+=String.fromCharCode((r&31)<<6|c2&63);n+=2}else{c2=e.charCodeAt(n+1);c3=e.charCodeAt(n+2);t+=String.fromCharCode((r&15)<<12|(c2&63)<<6|c3&63);n+=3}}return t}}
});

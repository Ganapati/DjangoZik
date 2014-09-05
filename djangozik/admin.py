from django.contrib import admin
from djangozik.models import Song, Album, Style, Artist, Playlist

admin.site.register(Song)
admin.site.register(Album)
admin.site.register(Style)
admin.site.register(Artist)
admin.site.register(Playlist)

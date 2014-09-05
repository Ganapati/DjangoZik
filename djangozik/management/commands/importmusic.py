# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.conf import settings
from djangozik.models import Song, Artist, Album, Style
import os
import fnmatch
import mutagen


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        self.stdout.write("Cleaning old songs")
        self.clean_songs()
        self.stdout.write("Scanning : %s" % settings.MUSIC_PATH)
        songs = []
        for root, dirs, files in os.walk(settings.MUSIC_PATH):
            for filename in fnmatch.filter(files, "*.mp3"):
                songs.append(os.path.join(root, filename))

        self.stdout.write("Parsing songs")
        for song in songs:
            tags = self.get_tags(song)

            try:
                artist = Artist.objects.filter(name=tags['artist'])
                album = Album.objects.filter(name=tags['album'])
                new_song = Song.objects.filter(title=tags['title'],
                                               artist=artist,
                                               album=album)
                if new_song.count() > 0:
                    continue
            except:
                pass

            self.stdout.write("+ %s : %s (%s, %s)" % (tags['artist'],
                                                      tags['title'],
                                                      tags['album'],
                                                      tags['genre']))

            artist = self.create_artist(tags['artist'],
                                        None)

            style = self.create_style(tags['genre'])

            album = self.create_album(tags['album'],
                                      tags['date'],
                                      None)

            songpath = song.replace(settings.MUSIC_PATH, '')

            self.create_song(tags['title'],
                             artist,
                             style,
                             album,
                             songpath)

        self.stdout.write("Scan finished")

    def clean_songs(self):
        songs = Song.objects.all()
        for song in songs:
            song_path = os.path.join(settings.MUSIC_PATH, song.filepath)
            if not os.path.isfile(song_path):
                self.stdout.write("- %s" % song)
                song.delete()

    def create_artist(self, artist, picture):
        artist, created = Artist.objects.get_or_create(name=artist,
                                                       picture=picture)
        if created:
            artist.save()
        return artist

    def create_style(self, name):
        style, created = Style.objects.get_or_create(name=name)
        if created:
            style.save()
        return style

    def create_album(self, album, date, picture):
        album, created = Album.objects.get_or_create(name=album,
                                                     date=date,
                                                     picture=picture)
        if created:
            album.save()
        return album

    def create_song(self, title, artist, style, album, song):
        song, created = Song.objects.get_or_create(title=title,
                                                   artist=artist,
                                                   style=style,
                                                   album=album,
                                                   filepath=song)
        if created:
            song.save()
        return song

    def get_tags(self, song):
        music = mutagen.File(song.decode('utf-8'), easy=True)

        title = "Unknown"
        date = "0000-00-00"
        album = "Unknown"
        genre = "Unknown"
        artist = "Unknown"

        if "title" in music.keys():
            title = music['title'][0].encode('utf-8').strip().capitalize()
        if "date" in music.keys():
            date = "%s-01-01" % music['date'][0].encode('utf-8').strip()
            if date == "0000-01-01":
                date = None
        if "album" in music.keys():
            album = music['album'][0].encode('utf-8').strip().capitalize()
        if "genre" in music.keys():
            genre = music['genre'][0].encode('utf-8').strip().capitalize()
        if "artist" in music.keys():
            artist = music['artist'][0].encode('utf-8').strip().capitalize()

        return {'title': title,
                'date': date,
                'album': album,
                'genre': genre,
                'artist': artist}

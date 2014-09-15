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

                song = os.path.join(root, filename)

                # If song exists, skip to the next
                song_path = song.replace(settings.MUSIC_PATH, '')
                nb_song = Song.objects.filter(filepath=song_path).count()
                if (nb_song > 0):
                    self.stdout.write("- %s already exists" % song_path.decode('utf-8',
                                                                               'ignore'))
                    continue

                tags = self.get_tags(song)

                # Check if a similar song exists
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

                # Visual output
                self.stdout.write("+ %s : %s (%s, %s)" % (tags['artist'].decode('utf-8',
                                                                                'ignore'),
                                                          tags['title'].decode('utf-8',
                                                                              'ignore'),
                                                          tags['album'].decode('utf-8',
                                                                              'ignore'),
                                                          tags['genre'].decode('utf-8',
                                                                              'ignore')))

                # Create artist if not exists
                artist = self.create_artist(tags['artist'],
                                            None)

                # Create style if not exists
                style = self.create_style(tags['genre'])

                # Create album if not exists
                album = self.create_album(tags['album'],
                                          tags['date'],
                                          None)

                songpath = song.replace(settings.MUSIC_PATH, '')

                if (songpath[0] == "/"):
                    songpath = songpath[1:]

                self.create_song(tags['title'],
                                 artist,
                                 style,
                                 album,
                                 songpath)

        self.stdout.write("Scan finished")

    def clean_songs(self):
        songs = Song.objects.all()
        for song in songs:
            relative_path = song.filepath
            if (relative_path[0] == "/"):
                relative_path = relative_path[1:]
            song_path = os.path.join(settings.MUSIC_PATH, relative_path)
            if not os.path.isfile(song_path):
                self.stdout.write("- %s" % song_path)
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

        title = song.decode('utf-8')
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

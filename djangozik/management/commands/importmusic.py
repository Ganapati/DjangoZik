# -*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand
from django.utils.encoding import smart_text
from django.conf import settings
from djangozik.models import Song, Artist, Album, Style
from libs.metadataGrabber import MetadataGrabber
import re
import os
import mutagen


class Command(NoArgsCommand):
    help = "Scan music folder and add new songs."

    def handle_noargs(self, **options):
        self.stdout.write("Cleaning old songs")
        self.stdout.write("Scanning : %s" % settings.MUSIC_PATH)
        songs = []
        for root, dirs, files in os.walk(settings.MUSIC_PATH):
            for filename in files:
                if not filename.endswith(('.mp3', '.ogg')) or filename.startswith('.'):
                    continue

                songs.append(os.path.join(root, filename))

                song = os.path.join(root, filename)

                # If song exists, skip to the next
                song_path = song.replace(settings.MUSIC_PATH, '')
                nb_song = Song.objects.filter(filepath=song_path).count()
                if (nb_song > 0):
                    self.stdout.write("skip %s " % song_path.decode('utf-8',
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
                frmt_str = "+ %s : %s (%s, %s)"
                self.stdout.write(frmt_str % (tags['artist'].decode('utf-8',
                                                                    'replace'),
                                              tags['title'].decode('utf-8',
                                                                   'replace'),
                                              tags['album'].decode('utf-8',
                                                                   'replace'),
                                              tags['genre'].decode('utf-8',
                                                                   'replace')))

                # Create artist if not exists
                artist = self.create_artist(tags['artist'],
                                            None)

                # Create style if not exists
                style = self.create_style(tags['genre'])

                # Create album if not exists
                album = self.create_album(tags['album'],
                                          tags['date'],
                                          None)

                songpath = smart_text(song.replace(settings.MUSIC_PATH, ''))

                if (songpath[0] == "/"):
                    songpath = songpath[1:]

                self.create_song(tags['title'],
                                 artist,
                                 style,
                                 album,
                                 songpath)

        self.stdout.write("Song scan finished")

        # Import artists
        self.stdout.write("Import artists")
        ImportArtists.import_artists()

        # Import covers
        self.stdout.write("Import covers")
        ImportCovers.import_covers()

        self.stdout.write("Scan finished")

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
        title = song.decode('utf-8', 'ignore')
        date = "0001-01-01"
        album = "Unknown"
        genre = "Unknown"
        artist = "Unknown"

        try:
            music = mutagen.File(smart_text(song), easy=True)
            if "title" in music.keys():
                title = music['title'][0].encode('utf-8').strip().capitalize()
            if "date" in music.keys():
                date = "%s-01-01" % music['date'][0].encode('utf-8').strip()
                regex = re.compile("^([0-9]{4}-[0-9]{2}-[0-9]{2})$")
                if not regex.match(date) or date == "0000-01-01":
                    date = None
            if "album" in music.keys():
                album = music['album'][0].encode('utf-8').strip().capitalize()
            if "genre" in music.keys():
                genre = music['genre'][0].encode('utf-8').strip().capitalize()
            if "artist" in music.keys():
                artist = music['artist'][0].encode('utf-8').strip().capitalize()
        except:
            # Use default values
            pass

        return {'title': title,
                'date': date,
                'album': album,
                'genre': genre,
                'artist': artist}


class ImportArtists():

    @staticmethod
    def import_artists():
        # Artists without pictures are considered as "new"
        artists = Artist.objects.filter(picture=None)
        metadata_grabber = MetadataGrabber()
        for artist in artists:
            try:
                infos = metadata_grabber.get_and_save_artist(artist.name,
                                                             "%s/%s" % (settings.STATIC_PATH,
                                                                        'images/artists/'),
                                                             "%s.jpg" % artist.slug)
                if infos is not None:
                    if 'infos' in infos.keys() and 'text' in infos['infos'].keys() and infos['infos']['text'] is not None:
                        artist.text = infos['infos']['text']
                    else:
                        artist.text = ""
                    if artist.slug is not None:
                        artist.picture = 'images/artists/%s.jpg' % artist.slug
                    else:
                        artist.picture = 'images/no_band.jpg'
                    artist.save()
            except:
                artist.picture = 'images/no_band.jpg'
                artist.text = ""
                artist.save()


class ImportCovers():

    @staticmethod
    def import_covers():
        # Albums with no cover are considered as "new"
        albums = Album.objects.filter(picture=None)
        metadata_grabber = MetadataGrabber()
        for album in albums:
            image = metadata_grabber.get_and_save_cover("%s" % album.name,
                                                        "%s/%s" % (settings.STATIC_PATH,
                                                                   'images/covers/'),
                                                        "%s.jpg" % album.slug)
            if image is not None:
                path = "%s%s.jpg" % ("images/covers/", album.slug)
            else:
                path = "images/no_cover.gif"
            album.picture = path
            album.save()

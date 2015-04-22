# -*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand
from djangozik.models import Song
from django.conf import settings
import os


class Command(NoArgsCommand):
    help = "Remove deleted songs from database."

    def handle_noargs(self, **options):
        songs = Song.objects.all()
        for song in songs:
            relative_path = song.filepath
            if (relative_path[0] == "/"):
                relative_path = relative_path[1:]
            song_path = os.path.join(settings.MEDIA_ROOT, relative_path)
            if not os.path.isfile(song_path):
                self.stdout.write("- %s" % song_path)
                song.delete()

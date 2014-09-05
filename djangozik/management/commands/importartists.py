# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from djangozik.models import Artist
from libs.metadataGrabber import MetadataGrabber
from django.conf import settings


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        self.stdout.write('Import picture and bio for artists')
        artists = Artist.objects.filter(picture=None)
        metadata_grabber = MetadataGrabber()
        for artist in artists:
            try:
                infos = metadata_grabber.get_and_save_artist(artist.name,
                                                             "%s/%s" % (settings.STATIC_PATH, 'images/artists/'),
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
                    self.stdout.write('+ %s' % artist.name)
            except:
                artist.picture = 'images/no_band.jpg'
                artist.text = ""
                artist.save()
                self.stdout.write('- %s' % artist.name)
        self.stdout.write('Import finished')

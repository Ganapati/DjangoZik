# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from djangozik.models import Album
from libs.metadataGrabber import MetadataGrabber
from django.conf import settings


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        self.stdout.write('Import covers for albums')
        albums = Album.objects.filter(picture=None)
        metadata_grabber = MetadataGrabber()
        for album in albums:
            image = metadata_grabber.get_and_save_cover("%s" % album.name,
                                                        "%s/%s" % (settings.STATIC_PATH, 'images/covers/'),
                                                        "%s.jpg" % album.slug)
            if image is not None:
                path = "%s%s.jpg" % ("images/covers/", album.slug)
            else:
                path = "images/no_cover.gif"
            album.picture = path
            album.save()
            self.stdout.write('+ %s' % album.name)
        self.stdout.write('Import finished')

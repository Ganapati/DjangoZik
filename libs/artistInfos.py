#!/usr/bin/python

import requests
import json
from django.conf import settings


class ArtistInfos:

    def __init__(self, url=None):
        if url is None:
            self.url = "https://api.discogs.com/database/search?type=artist&q=%s&key=%s&secret=%s"
        else:
            self.url = url

    def get(self, artist):
        data = {'success': False,
                'infos': None}
        headers = {'User-Agent': 'DjangoZik - opensource web player - dev'}
        infos = requests.get(self.url % (artist, settings.DISCOGS_KEY, settings.DISCOGS_SECRET),
                             headers=headers)
        if infos.status_code == 200:
            try:
                json_infos = json.loads(infos.text)
                if json_infos['pagination']['items'] != 0:
                    data['success'] = True
                    data['infos'] = {'image': json_infos['results'][0]['thumb'],
                                    'text': json_infos['results'][0]['title']}
            except:
                # return data the next line
                pass

        return data

if __name__ == "__main__":
    print "Get artist infos"
    artist_infos = ArtistInfos()
    infos = artist_infos.get("les muscles")
    if infos['infos'] is not None:
        print infos
    else:
        print "Error"

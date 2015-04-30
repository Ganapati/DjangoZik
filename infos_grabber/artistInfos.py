#!/usr/bin/python

import requests
import json
from django.conf import settings
import bbcode


class ArtistInfos:
    def __init__(self, url=None, url_info=None):
        if url is None:
            self.url = "https://api.discogs.com/database/search"
            self.url_info = "https://api.discogs.com/artists/%d"
        else:
            self.url = url
            self.url_info = url_info

    def get(self, artist):
        data = {'success': False, 'infos': None}
        params = {
            'type': 'artist',
            'q': artist,
            'page': 1,
            'per_page': 1,
            'key': settings.DISCOGS_KEY,
            'secret': settings.DISCOGS_SECRET
        }
        headers = {'User-Agent': 'DjangoZik - opensource web player - dev'}
        infos = requests.get(self.url, params=params, headers=headers, verify=False)
        if infos.status_code == 200:
            try:
                data['success'] = True
                json_infos = json.loads(infos.text)
                params = {
                    'key': settings.DISCOGS_KEY,
                    'secret': settings.DISCOGS_SECRET
                }

                details = requests.get(self.url_info %
                                       json_infos['results'][0]['id'],
                                       params=params,
                                       headers=headers)
                json_details = json.loads(details.text)
                data['infos'] = {
                    'image': json_infos['results'][0]['thumb'],
                    'text': bbcode.render_html(json_details['profile'])
                }
            except:
                # return data the next line
                pass

        return data


if __name__ == "__main__":
    print "Get artist infos"
    artist_infos = ArtistInfos()
    infos = artist_infos.get("Nirvana")
    if infos['infos'] is not None:
        print infos
    else:
        print "Error"

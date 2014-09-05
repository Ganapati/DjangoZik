#!/usr/bin/python

import requests
import json


class ArtistInfos:

    def __init__(self, url=None):
        if url is None:
            self.url = "http://api.discogs.com/search?f=json&type=artist&q="
        else:
            self.url = url

    def get(self, artist):
        data = {'success': False,
                'infos': None}
        headers = {'User-Agent': 'DjangoZik - opensource web player - dev'}
        infos = requests.get("%s%s" % (self.url, artist), headers=headers)
        if infos.status_code == 200:
            try:
                json_infos = json.loads(infos.text)
                if json_infos['resp']['status']:
                    data['success'] = True
                    data['infos'] = {'image': json_infos['resp']['search']['searchresults']['results'][0]['thumb'].encode('utf-8'),
                                    'text': json_infos['resp']['search']['searchresults']['results'][0]['summary'].encode('utf-8')}
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

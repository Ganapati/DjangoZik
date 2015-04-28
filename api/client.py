import requests
import json


class ApiClient(object):
    def __init__(self, endpoint=None, key=None):
        self.api_path = '/api/%s'
        self.endpoint = endpoint if endpoint[-1] != '/' else endpoint[:-1]
        self.remote_media = "%s%s" % (self.endpoint, '/media/')
        self.remote_static = "%s%s" % (self.endpoint, '/static/')
        self.key = key

    def songs(self, album=None, artist=None):
        if album is not None:
            songs = self.request('song', {'album': album})
        elif artist is not None:
            songs = self.request('song', {'artist': artist})
        else:
            songs = {}
        return songs

    def albums(self, artist=None):
        if artist is not None:
            albums = self.request('album', {'artist': artist})
        else:
            albums = self.request('album')
        return albums

    def artists(self, style=None):
        if style is not None:
            artists = self.request('artist', {'style': style})
        else:
            artists = self.request('artist')
        return artists

    def styles(self):
        styles = self.request('style')
        return styles

    def search(self, keyword=None):
        if keyword is not None:
            search = self.request('search', {'keyword': keyword})
        else:
            search = {}
        return search

    def request(self, data_type, params={}):
        try:
            params['key'] = self.key
            path = "%s%s" % (self.endpoint, (self.api_path % data_type))
            response = requests.get(path, params=params)
            if response.status_code == 200:
                data = response.text
                # Add full domain name to relative resource path
                data = data.replace('#media#', self.remote_media)
                data = data.replace('#static#', self.remote_static)
                json_data = json.loads(data)
                return json_data
            else:
                raise Exception()
        except:
            return {}

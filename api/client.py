import requests
import json


class ApiClient(object):
    def __init__(self, endpoint=None, key=None):
        self.api_path = '/api/%(type)s'
        self.endpoint = endpoint if endpoint[-1] != '/' else endpoint[:-1]
        self.remote_media = "%s%s" % (self.endpoint, '/media/')
        self.remote_static = "%s%s" % (self.endpoint, '/static/')
        self.key = key

    def albums(self, slug=None):
        if slug is not None:
            albums = self.request('album', {'slug': slug})
            if bool(albums):
                albums['album']['picture'] = "%s%s" % (
                    self.remote_static, albums['album']['picture']
                )
                for index, song in enumerate(albums['songs']):
                    full_path = "%s%s" % (self.remote_media, song['filepath'])
                    albums['songs'][index]['filepath'] = full_path
                for index, artist in enumerate(albums['artists']):
                    albums['artists'][index]['picture'] = "%s%s" % (
                        self.remote_static,
                        albums['artists'][index]['picture'])
        else:
            albums = self.request('album')
            if bool(albums):
                for index, album in enumerate(albums['albums']):
                    albums['albums'][index]['picture'] = "%s%s" % (
                        self.remote_static, albums['albums'][index]['picture']
                    )
        return albums

    def artist(self, slug=None):
        if slug is not None:
            artists = self.request('artist', {'slug': slug})
            if bool(artists):
                artists['artist']['picture'] = "%s%s" % (
                    self.remote_static, artists['artist']['picture']
                )
                for index, album in enumerate(artists['albums']):
                    full_path = "%s%s" % (self.remote_static, album['picture'])
                    artists['albums'][index]['filepath'] = full_path
                for index, song in enumerate(artists['songs']):
                    full_path = "%s%s" % (self.remote_media, song['filepath'])
                    artists['songs'][index]['filepath'] = full_path

        else:
            artists = self.request('artist')
            if bool(artists):
                for index, artist in enumerate(artists['artists']):
                    artists['artists'][index]['picture'] = "%s%s" % (
                        self.remote_static,
                        artists['artists'][index]['picture'])

        return artists

    def style(self, slug=None):
        if slug is not None:
            styles = self.request('style', {'slug': slug})
            if bool(styles):
                for index, artist in enumerate(styles['artists']):
                    styles['artists'][index]['picture'] = "%s%s" % (
                        self.remote_static, styles['artists'][index]['picture']
                    )
        else:
            styles = self.request('style')
        return styles

    def search(self, keyword=None):
        if keyword is not None:
            search = self.request('search', {'keyword': keyword})
        else:
            search = self.request('search')

        if bool(search):
            if 'songs' in search.keys():
                for index, song in enumerate(search['songs']):
                    full_path = "%s%s" % (self.remote_media, song.filepath)
                    search['songs'][index]['filepath'] = full_path
                for index, artist in enumerate(search['artists']):
                    search['artists'][index]['picture'] = "%s%s" % (
                        self.remote_static, search['artists'][index]['picture']
                    )
                for index, album in enumerate(search['albums']):
                    search['albums'][index]['picture'] = "%s%s" % (
                        self.remote_static, search['albums'][index]['picture']
                    )

        return search

    def request(self, data_type, params={}):
        try:
            params['key'] = self.key
            path = "%s%s" % (self.endpoint, self.api_path % data_type)
            response = requests.get(path, params=params)
            if response.status_code == 200:
                return json.dumps(response.text)
            else:
                raise Exception()
        except:
            return {}

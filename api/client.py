import grequests
from requests import Response
import json


class ApiClient(object):
    def songs(self, album=None, artist=None, instances=[]):
        if album is not None:
            songs = self.request('song', {'album': album}, instances)
        elif artist is not None:
            songs = self.request('song', {'artist': artist}, instances)
        else:
            songs = {}
        return songs

    def albums(self, artist=None, instances=[]):
        if artist is not None:
            albums = self.request('album', {'artist': artist}, instances)
        else:
            albums = self.request('album', instances=instances)
        return albums

    def artists(self, style=None, instances=[]):
        if style is not None:
            artists = self.request('artist', {'style': style}, instances)
        else:
            artists = self.request('artist', instances=instances)
        return artists

    def styles(self, instances=[]):
        styles = self.request('style', instances=instances)
        return styles

    def search(self, keyword=None, instances=[]):
        if keyword is not None:
            search = self.request('search', {'keyword': keyword}, instances)
        else:
            search = {}
        return search

    def request(self, data_type, params={}, instances=[]):
        api_path = '/api/%s'
        try:
            urls = []
            for instance in instances:
                if instance.url[-1] != '/':
                    endpoint = instance.url
                else:
                    endpoint = instance.url[:-1]
                remote_media = "%s%s" % (endpoint, '/media/')
                remote_static = "%s%s" % (endpoint, '/static/')
                path = "%s%s" % (endpoint, (api_path % data_type))
                urls.append({'url': path,
                             'params': {'key': instance.key},
                             'url_static': remote_static,
                             'url_media': remote_media})

            rs = [grequests.get(u['url'],
                                params=u['params'],
                                hooks={'response': [self.hook_factory(
                                                url_media=u['url_media'],
                                                url_static=u['url_static'])
                                            ]}) for u in urls]
            responses = grequests.map(rs, size=5)
            json_data = {}
            for response in responses:
                try:
                    json_data.update(json.loads(response.text))
                except:
                    pass
            return json_data
        except:
            return {}

    def hook_factory(self, *factory_args, **factory_kwargs):
        def response_hook(response, *request_args, **request_kwargs):
            if response.status_code == 200:
                url_media = factory_kwargs['url_media']
                url_static = factory_kwargs['url_static']
                data = response.text.replace('#media#', url_media)
                data = data.replace('#static#', url_static)
                response._content = data.encode('utf-8')
                return response
            return ''
        return response_hook

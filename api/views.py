from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from djangozik.models import Album, Artist, Song, Style
from api.models import ApiKey
from rest_framework_extensions.cache.decorators import cache_response


class DjangoZikAPIView(APIView):
    def calculate_cache_key(self, view_instance, view_method,
                            request, args, kwargs):
            return '.'.join([
                '.'.join(request.GET),
                request.path
            ])


class ArtistApiView(DjangoZikAPIView):
    @cache_response(60 * 15, key_func='calculate_cache_key')
    def get(self, request):
        get_object_or_404(ApiKey, key=request.GET.get('key', None))
        api_response = ApiResponse()
        content = {}
        try:
            style = request.GET.get('style', None)
            if style is not None:
                content['artists'] = Artist.objects.filter(
                    song__style__slug=style).values('name', 'slug', 'picture',
                                                    'text')
                for artist in content['artists']:
                    artist['picture'] = "%s%s" % ('#static#',
                                                  artist['picture'])
            else:
                content['artists'] = Artist.objects.all().values(
                    'name', 'slug', 'picture', 'text')
                for artist in content['artists']:
                    artist['picture'] = "%s%s" % ('#static#',
                                                  artist['picture'])
            api_response.set_content(content)
        except:
            api_response.content = ''
            api_response.status = status.HTTP_404_NOT_FOUND
        return Response(api_response.content, api_response.status)


class SearchApiView(DjangoZikAPIView):
    @cache_response(60 * 15, key_func='calculate_cache_key')
    def get(self, request):
        get_object_or_404(ApiKey, key=request.GET.get('key', None))
        api_response = ApiResponse()
        keyword = request.GET.get('keyword', None)
        content = {}

        try:
            artists = Artist.objects.filter(name__icontains=keyword).values(
                'name', 'slug', 'text', 'picture')
            for artist in artists:
                artist['picture'] = "%s%s" % ('#static#', artist['picture'])
        except Artist.DoesNotExist:
            artists = []

        try:
            albums = Album.objects.filter(name__icontains=keyword).values(
                'name', 'date', 'picture', 'slug')
            for album in albums:
                album['picture'] = "%s%s" % ('#static#', album['picture'])
        except Album.DoesNotExist:
            albums = []

        try:
            songs = Song.objects.filter(title__icontains=keyword).values(
                'title', 'filepath', 'slug', 'album__name', 'album__slug',
                'album__picture', 'artist__name', 'artist__slug',
                'style__slug', 'style__name')
            for song in songs:
                song['filepath'] = "%s%s" % ('#media#', song['filepath'])
                song['album_picture'] = "%s%s" % ('#static#',
                                                  song['album_picture'])

        except Song.DoesNotExist:
            songs = []

        content['artists'] = artists
        content['albums'] = albums
        content['songs'] = songs
        api_response.set_content(content)
        return Response(api_response.content, api_response.status)


class AlbumApiView(DjangoZikAPIView):
    @cache_response(60 * 15, key_func='calculate_cache_key')
    def get(self, request):
        get_object_or_404(ApiKey, key=request.GET.get('key', None))
        api_response = ApiResponse()
        content = {}
        try:
            artist = request.GET.get('artist', None)
            if artist is not None:
                content['albums'] = Album.objects.filter(
                    song__artist__slug=artist).values('name',
                                                      'slug',
                                                      'picture')
                for album in content['albums']:
                    album['picture'] = "%s%s" % ('#static#', album['picture'])
            else:
                content['albums'] = Album.objects.all().values('name', 'slug',
                                                               'picture')
                for album in content['albums']:
                    album['picture'] = "%s%s" % ('#static#', album['picture'])

            api_response.set_content(content)
        except:
            api_response.content = ''
            api_response.status = status.HTTP_404_NOT_FOUND

        return Response(api_response.content, api_response.status)


class StyleApiView(DjangoZikAPIView):
    @cache_response(60 * 15, key_func='calculate_cache_key')
    def get(self, request):
        get_object_or_404(ApiKey, key=request.GET.get('key', None))
        api_response = ApiResponse()
        content = {}
        try:
            content['styles'] = Style.objects.all().values('name', 'slug')
            api_response.set_content(content)
        except:
            api_response.content = ''
            api_response.status = status.HTTP_404_NOT_FOUND

        return Response(api_response.content, api_response.status)


class SongApiView(DjangoZikAPIView):
    @cache_response(60 * 15, key_func='calculate_cache_key')
    def get(self, request):
        get_object_or_404(ApiKey, key=request.GET.get('key', None))
        api_response = ApiResponse()
        album = request.GET.get('album', None)
        artist = request.GET.get('artist', None)
        content = {}
        try:
            if album is not None:
                content['songs'] = Song.objects.filter(
                    album__slug=album).values(
                        'slug', 'title', 'filepath', 'album__name',
                        'album__slug', 'album__picture', 'artist__name',
                        'artist__slug', 'style__name', 'style__slug')
                for song in content['songs']:
                    song['filepath'] = "%s%s" % ('#media#', song['filepath'])
                    song['album__picture'] = "%s%s" % ('#static#',
                                                       song['album__picture'])

                api_response.set_content(content)
            if artist is not None:
                content['songs'] = Song.objects.filter(
                    artist__slug=artist).values(
                        'slug', 'title', 'filepath', 'album__name',
                        'album__slug', 'album__picture', 'artist__name',
                        'artist__slug', 'style__name', 'style__slug')
                for song in content['songs']:
                    song['filepath'] = "%s%s" % ('#media#', song['filepath'])
                    song['album__picture'] = "%s%s" % ('#static#',
                                                       song['album__picture'])

                api_response.set_content(content)
            if album is None and artist is None:
                api_response.content = ''
                api_response.status = status.HTTP_404_NOT_FOUND
        except:
            api_response.content = ''
            api_response.status = status.HTTP_404_NOT_FOUND

        return Response(api_response.content, api_response.status)


class ApiResponse(object):
    def __init__(self):
        self.status = status.HTTP_200_OK
        self.content = ''

    def set_content(self, content):
        if not content:
            self.content = {'detail': 'Not found'}
            self.status = status.HTTP_404_NOT_FOUND
        else:
            self.content = content

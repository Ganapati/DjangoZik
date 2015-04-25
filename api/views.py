from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from djangozik.models import Album, Artist, Song, Style
from api.models import ApiKey


class ArtistApiView(APIView):
    def get(self, request):
        get_object_or_404(ApiKey, key=request.GET.get('key', None))
        api_response = ApiResponse()
        content = {}
        try:
            style = request.GET.get('style', None)
            if style is not None:
                content['artists'] = Artist.objects.filter(
                    song__style=style).values('name', 'slug', 'picture',
                                              'text')
            else:
                content['artists'] = Artist.objects.all().values(
                    'name', 'slug', 'picture', 'text')
            api_response.set_content(content)
        except:
            api_response.content = ''
            api_response.status = status.HTTP_404_NOT_FOUND
        return Response(api_response.content, api_response.status)


class SearchApiView(APIView):
    def get(self, request):
        get_object_or_404(ApiKey, key=request.GET.get('key', None))
        api_response = ApiResponse()
        keyword = request.GET.get('keyword', None)
        content = {}

        try:
            artists = Artist.objects.filter(name__icontains=keyword).values(
                'name', 'slug', 'text', 'picture')
        except Artist.DoesNotExist:
            artists = []

        try:
            albums = Album.objects.filter(name__icontains=keyword).values(
                'name', 'date', 'picture', 'slug')
        except Album.DoesNotExist:
            albums = []

        try:
            songs = Song.objects.filter(title__icontains=keyword).values(
                'title', 'filepath', 'slug', 'album__name', 'album__slug',
                'artist__name', 'artist__slug')
        except Song.DoesNotExist:
            songs = []

        content['artists'] = artists
        content['albums'] = albums
        content['songs'] = songs
        api_response.set_content(content)
        return Response(api_response.content, api_response.status)


class AlbumApiView(APIView):
    def get(self, request):
        get_object_or_404(ApiKey, key=request.GET.get('key', None))
        api_response = ApiResponse()
        content = {}
        try:
            artist = request.GET.get('artist', None)
            if artist is not None:
                content['albums'] = Album.objects.fiter(
                    artist__slug=artist).values('name', 'slug', 'picture',
                                                'artist__name', 'artist__slug')
            else:
                content['albums'] = Album.objects.all().values(
                    'name', 'slug', 'picture', 'artist__name', 'artist__slug')
            api_response.set_content(content)
        except:
            api_response.content = ''
            api_response.status = status.HTTP_404_NOT_FOUND

        return Response(api_response.content, api_response.status)


class StyleApiView(APIView):
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


class SongApiView(APIView):
    def get(self, request):
        get_object_or_404(ApiKey, key=request.GET.get('key', None))
        api_response = ApiResponse()
        album = request.GET.get('album', None)
        artist = request.GET.get('artist', None)
        content = {}
        try:
            if album is not None:
                content['songs'] = Song.objects.filter(
                    album__slug=album).values('slug', 'title', 'filepath',
                                              'album__name', 'album__slug',
                                              'artist__name', 'artist__slug')
            if artist is not None:
                content['songs'] = Song.objects.filter(
                    artist__slug=artist).values('slug', 'title', 'filepath',
                                                'album__name', 'album__slug',
                                                'artist__name', 'artist__slug')
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

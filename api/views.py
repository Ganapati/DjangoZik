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
        slug = request.GET.get('slug', None)
        content = {}
        try:
            if slug is not None:
                artist = Artist.objects.get(slug=slug)
                content['artist'] = {
                    'name': artist.name,
                    'slug': artist.slug,
                    'text': artist.text,
                    'picture': artist.picture
                }
                content['albums'] = Album.objects.filter(
                    song__artist=artist).distinct().values('name', 'date',
                                                           'picture', 'slug')
                content['songs'] = Song.objects.filter(
                    artist=artist).distinct().values('title', 'filepath',
                                                     'slug')
            else:
                content = Artist.objects.all().values('name', 'slug')
            api_response.set_content(content)
        except KeyError:
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
                'title', 'filepath', 'slug')
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
        slug = request.GET.get('slug', None)
        content = {}
        try:
            if slug is not None:
                album = Album.objects.get(slug=slug)
                content['album'] = {
                    'name': album.name,
                    'slug': album.slug,
                    'date': album.date,
                    'picture': album.picture
                }
                content['songs'] = Song.objects.filter(album=album).values(
                    'title', 'filepath', 'slug')
                content['artist'] = Artist.objects.filter(album=album).values(
                    'name', 'slug', 'text', 'picture')
            else:
                content['albums'] = Album.objects.all().values('name', 'date',
                                                               'picture',
                                                               'slug')
            api_response.set_content(content)
        except:
            api_response.content = ''
            api_response.status = status.HTTP_404_NOT_FOUND

        return Response(api_response.content, api_response.status)


class StyleApiView(APIView):
    def get(self, request):
        get_object_or_404(ApiKey, key=request.GET.get('key', None))
        api_response = ApiResponse()
        slug = request.GET.get('slug', None)
        content = {}
        try:
            if slug is not None:
                style = Style.objects.get(slug=slug)
                content['style'] = {'name': style.name, 'slug': style.slug}
                content['artists'] = Artist.objects.filter(
                    song__style=style).distinct().values('name', 'slug',
                                                         'text', 'picture')
            else:
                content['styles'] = Style.objects.all().values('name', 'slug')
            api_response.set_content(content)
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

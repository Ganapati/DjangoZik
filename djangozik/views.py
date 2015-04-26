import json
from django.http import HttpResponse
from django.views.generic import TemplateView
from djangozik.models import Song, Artist, Album, Playlist, Style, Radio
from django.views.generic.detail import BaseDetailView
from django.db.models import Count
import base64
from api.client import ApiClient
from api.models import RemoteInstance


class DjangoZikView(TemplateView):
    def merge_dict(self, d1, d2):
        d1 = [entry for entry in d1]
        for item in d2:
            l = [i.values() for i in d1]
            if item['slug'] not in [item for sublist in l for item in sublist]:
                d1.append(item)
        return d1


class HomeView(DjangoZikView):

    template_name = "djangozik/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['songs'] = Song.objects.order_by('-id')[:10]
        context['active'] = "home"
        styles = Style.objects.values('name').annotate(Count('song')).order_by(
            '-song__count')
        context['stats_styles'] = styles[:10]
        context['nb_artists'] = Artist.objects.all().count()
        context['nb_songs'] = Song.objects.all().count()
        context['nb_albums'] = Album.objects.all().count()
        context['nb_styles'] = Style.objects.all().count()
        context['nb_peers'] = RemoteInstance.objects.all().count()
        context['modal_playlists'] = Playlist.objects.all()
        return context


class SongsView(DjangoZikView):
    template_name = "djangozik/songs.html"

    def get_context_data(self, **kwargs):
        context = super(SongsView, self).get_context_data(**kwargs)

        remote_instances = RemoteInstance.objects.all()
        songs = []

        if self.kwargs['type'] == 'album':
            album = Album.objects.filter(slug=self.kwargs['key'])
            context['album'] = album
            songs = Song.objects.filter(album__in=album).values(
                'title', 'slug', 'filepath', 'album__slug', 'album__name', 'album__picture',
                'artist__name', 'artist__slug', 'style__name', 'style__slug')
            for remote_instance in remote_instances:
                api_client = ApiClient(remote_instance.url,
                                       remote_instance.key)
                remote_songs = api_client.songs(album=self.kwargs['key'])
                songs = self.merge_dict(songs, remote_songs['songs'])

        elif self.kwargs['type'] == 'playlist':
            playlist = Playlist.objects.get(slug=self.kwargs['key'])
            context['playlist'] = playlist
            songs = Song.objects.filter(playlist=playlist).values(
                'title', 'slug', 'filepath', 'album__slug', 'album__name', 'album__picture',
                'artist__name', 'artist__slug', 'style__name', 'style__slug')

        elif self.kwargs['type'] == 'artist':
            artist = Artist.objects.filter(slug=self.kwargs['key'])
            context['artist'] = artist
            songs = Song.objects.filter(artist=artist).order_by(
                'album__name').values('title', 'slug', 'filepath',
                                      'album__slug', 'album__name', 'album__picture',
                                      'artist__name', 'artist__slug',
                                      'style__name', 'style__slug')

            for remote_instance in remote_instances:
                api_client = ApiClient(remote_instance.url,
                                       remote_instance.key)
                remote_songs = api_client.songs(artist=self.kwargs['key'])
                songs = self.merge_dict(songs, remote_songs['songs'])

        context['type'] = self.kwargs['type']
        context['songs'] = songs
        context['active'] = "songs"
        context['modal_playlists'] = Playlist.objects.all()
        return context


class ArtistsView(DjangoZikView):

    template_name = "djangozik/artists.html"

    def get_context_data(self, **kwargs):
        context = super(ArtistsView, self).get_context_data(**kwargs)

        remote_instances = RemoteInstance.objects.all()
        style = None
        if 'style' in self.kwargs.keys() and self.kwargs['style'] is not None:
            try:
                style = Style.objects.filter(slug=self.kwargs['style'])
                context['artists'] = Artist.objects.filter(
                    song__style__in=style).distinct().values('name', 'slug',
                                                             'text', 'picture')
                for remote_instance in remote_instances:
                    api_client = ApiClient(remote_instance.url,
                                           remote_instance.key)
                    remote_artists = api_client.artists(
                        style=self.kwargs['style'])
                    context['artists'] = self.merge_dict(
                        context['artists'], remote_artists['artists'])

            except Style.DoesNotExist:
                context['artists'] = []
        else:
            context['artists'] = Artist.objects.all().values('name', 'slug',
                                                             'text', 'picture')
            for remote_instance in remote_instances:
                api_client = ApiClient(remote_instance.url,
                                       remote_instance.key)
                remote_artists = api_client.artists()
                context['artists'] = self.merge_dict(context['artists'],
                                                     remote_artists['artists'])

        context['active'] = "artists"
        context['modal_playlists'] = Playlist.objects.all()
        return context


class AlbumsView(DjangoZikView):

    template_name = "djangozik/albums.html"

    def get_context_data(self, **kwargs):
        context = super(AlbumsView, self).get_context_data(**kwargs)

        remote_instances = RemoteInstance.objects.all()
        artist = None
        context['artists'] = None
        if ('artist' in self.kwargs.keys() and
            self.kwargs['artist'] is not None):
            try:
                artist = Artist.objects.filter(slug=self.kwargs['artist'])
                context['artists'] = artist
                context['albums'] = Album.objects.filter(
                    song__artist__in=artist).distinct().values('picture',
                                                               'slug', 'name')
                for remote_instance in remote_instances:
                    api_client = ApiClient(remote_instance.url,
                                           remote_instance.key)
                    remote_albums = api_client.albums(
                        artist=self.kwargs['artist'])
                    context['albums'] = self.merge_dict(
                        context['albums'], remote_albums['albums'])

            except Artist.DoesNotExist:
                context['albums'] = []
        else:
            context['albums'] = Album.objects.all().values('picture', 'slug',
                                                           'name')
            for remote_instance in remote_instances:
                api_client = ApiClient(remote_instance.url,
                                       remote_instance.key)
                remote_albums = api_client.albums()
                context['albums'] = self.merge_dict(context['albums'],
                                                    remote_albums['albums'])

        context['active'] = "albums"
        context['modal_playlists'] = Playlist.objects.all()
        return context


class StylesView(DjangoZikView):

    template_name = "djangozik/styles.html"

    def get_context_data(self, **kwargs):
        context = super(StylesView, self).get_context_data(**kwargs)
        context['styles'] = Style.objects.all().values('name', 'slug')

        remote_instances = RemoteInstance.objects.all()
        for remote_instance in remote_instances:
            api_client = ApiClient(remote_instance.url, remote_instance.key)
            remote_styles = api_client.styles()
            context['styles'] = self.merge_dict(context['styles'],
                                                remote_styles['styles'])

        context['active'] = "styles"
        context['modal_playlists'] = Playlist.objects.all()
        return context


class PlaylistsView(DjangoZikView):

    template_name = "djangozik/playlists.html"

    def get_context_data(self, **kwargs):
        context = super(PlaylistsView, self).get_context_data(**kwargs)
        context['playlists'] = Playlist.objects.all()
        context['modal_playlists'] = Playlist.objects.all()
        context['active'] = "playlists"
        return context


class RadiosView(DjangoZikView):

    template_name = "djangozik/radios.html"

    def get_context_data(self, **kwargs):
        context = super(RadiosView, self).get_context_data(**kwargs)
        context['radios'] = Radio.objects.all()
        context['modal_playlists'] = Playlist.objects.all()
        context['active'] = "radios"
        return context


class SearchView(DjangoZikView):

    template_name = "djangozik/search.html"

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        keyword = self.kwargs['keyword']

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

        try:
            playlists = Playlist.objects.filter(name__icontains=keyword)
        except Playlist.DoesNotExist:
            playlists = []

        remote_instances = RemoteInstance.objects.all()
        for remote_instance in remote_instances:
            api_client = ApiClient(remote_instance.url, remote_instance.key)
            search = api_client.search(keyword)
            artists = self.merge_dict(artists, search['artists'])
            songs = self.merge_dict(songs, search['songs'])
            albums = self.merge_dict(albums, search['albums'])

        context['artists'] = artists
        context['albums'] = albums
        context['songs'] = songs
        context['playlists'] = playlists
        context['modal_playlists'] = Playlist.objects.all()

        context['active'] = "search"
        return context


class AjaxView(BaseDetailView):
    def get(self, request, *args, **kwargs):
        method = self.kwargs['method']
        arg = self.kwargs['arg']

        success = False
        message = ""

        # Add a song to playlist
        if method == "playlist":
            try:
                (playlist_slug, song_slug) = arg.split("::")
                song = Song.objects.get(slug=song_slug)
                playlist = Playlist.objects.get(slug=playlist_slug)
                playlist.songs.add(song)
                playlist.save()
                success = True
            except:
                # Return False if error happend
                pass

        # Delete Radio
        if method == "delete_radio":
            try:
                Radio.objects.get(pk=arg).delete()
                success = True
            except:
                # Return False if error happend
                pass

        # Delete a playlist
        if method == "delete_playlist":
            try:
                Playlist.objects.get(slug=arg).delete()
                success = True
            except:
                # Return False if error happend
                pass

        # Remove Song from playlist
        if method == "remove_song_from_playlist":
            try:
                (song_slug, playlist_slug) = arg.split("::")
                song = Song.objects.get(slug=song_slug)
                playlist = Playlist.objects.get(slug=playlist_slug)
                playlist.songs.remove(song)
                playlist.save()
                success = True
            except:
                # Return False if error happend
                pass

        # Add a radio
        if method == "add_radio":
            try:
                try:
                    nb_radio = Radio.objects.get(
                        url=base64.b64decode(arg)).count()
                    if nb_radio > 0:
                        raise Exception("Already exists")
                except Radio.DoesNotExist:
                    # Good, Radio does not exists
                    pass
                radio = Radio()
                radio.url = base64.b64decode(arg)
                radio.save()
                message = {"url": radio.url, "id": radio.id}
                success = True
            except:
                # Return False if error happened
                pass

        # Add a playlist
        if method == "add_playlist":
            try:
                nb_playlist = Playlist.objects.get(name=arg).count()
                if nb_playlist > 0:
                    raise Exception("Already exists")
                playlist = Playlist()
                playlist.name = arg
                playlist.save()
                message = {"slug": playlist.slug, "name": playlist.name}
                success = True
            except:
                # Return false if error happened
                pass

        data = {"success": success, "message": message}

        return self.render_to_json_response(data)

    def render_to_json_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        return HttpResponse(json.dumps(context),
                            content_type='application/json', **response_kwargs)

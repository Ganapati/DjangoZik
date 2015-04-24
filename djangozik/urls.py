from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic.base import RedirectView

from djangozik.views import HomeView, ArtistsView
from djangozik.views import AlbumsView, StylesView
from djangozik.views import PlaylistsView, SearchView
from djangozik.views import SongsView, RadiosView
from djangozik.views import AjaxView

from guitar_tabs.views import GuitarTabsView

admin.autodiscover()

urlpatterns = patterns(
    '', url(r'^$', login_required(HomeView.as_view()), name='home'),
        url(r'^songs/(?P<type>[^/]+)/(?P<key>[^/]+)$',
                              login_required(SongsView.as_view()),
                              name='songs'),
        url(r'^artists/(?P<style>[^/]+)?$', login_required(ArtistsView.as_view()),
            name='artists'),
        url(r'^albums/(?P<artist>[^/]+)?$',
                             login_required(AlbumsView.as_view()),
                             name='albums'),
        url(r'^styles/(?P<style>[^/]+)?$', login_required(StylesView.as_view()),
            name='styles'),
        url(r'^playlists/(?P<playlist>[^/]+)?$',
                            login_required(PlaylistsView.as_view()),
                            name='playlists'),
        url(r'^radios/(?P<radio>[^/]+)?$', login_required(RadiosView.as_view()),
            name='radios'),
        url(r'^search/(?P<keyword>[^/]+)$', login_required(SearchView.as_view()),
            name='search'), url('^accounts/login', 'django.contrib.auth.views.login',
                                name='login'),
        url('^accounts/logout', 'django.contrib.auth.views.logout',
            {'next_page': '/'},
            name='logout'),
        url('^ajax/(?P<method>[^/]+)/(?P<arg>[^/]+)',
                                login_required(AjaxView.as_view()),
                                name='ajax'),
        url(r'^admin/', include(admin.site.urls)),
        url(r'^api/', include('api.urls')),
        url(r'^tab/$', login_required(GuitarTabsView.as_view()),
            name="tab"),
        url(r'^favicon\.', RedirectView.as_view(url='/static/favicon.ico'))
    ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

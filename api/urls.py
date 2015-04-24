# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from api.views import ArtistApiView, AlbumApiView, StyleApiView, SearchApiView

# Authentication
urlpatterns = patterns('',
                       url(r'^artist/?$',
                           ArtistApiView.as_view(),
                           name='api_artists'),
                       url(r'^album/?$',
                           AlbumApiView.as_view(),
                           name='api_album'),
                       url(r'^style/?$',
                           StyleApiView.as_view(),
                           name='api_style'),
                       url(r'^search/?$',
                           SearchApiView.as_view(),
                           name='api_search'),
                       )

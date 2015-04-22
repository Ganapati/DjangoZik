# -*- coding: utf-8 -*-

from django.views.generic import TemplateView
from django.shortcuts import render
from guitar_tabs.tab_grabber import TabGrabber


class GuitarTabsView(TemplateView):
    template_name = "guitar_tabs/tab.html"

    def get(self, request):
        tab_grabber = TabGrabber()
        song_name = request.GET.get('song', None)
        if song_name is not None:
            tab = tab_grabber.search(song_name)
        else:
            tab = None
        return render(request,
                      self.template_name,
                      {'tab': tab})

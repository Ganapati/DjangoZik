#!/usr/bin/python

import requests
from bs4 import BeautifulSoup


class TabGrabber:

    def __init__(self, search_url=None):
        if search_url is None:
            self.search_url = 'http://www.ultimate-guitar.com/search.php?search_type=title&value='
        else:
            self.search_url = search_url

    def request_service(self, keyword):
        complete_url = "%s%s" % (self.search_url, keyword)
        html = requests.get(complete_url)
        soup = BeautifulSoup(html.text)
        return soup

    def grab(self, keyword):
        # try:
        return None
        # except:
        #    return None

if __name__ == "__main__":
    print "Tablatures grabber"
    tab_grabber = TabGrabber()

    tab = tab_grabber.grab('Highway to hell')
    if tab is None:
        print "Error"
    else:
        print "tab : %s" % tab

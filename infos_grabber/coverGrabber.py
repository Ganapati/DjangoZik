#!/usr/bin/python

import requests
from bs4 import BeautifulSoup


class CoverGrabber:
    def __init__(self, url=None):
        if url is None:
            self.url = 'http://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias=aps&field-keywords=cd'
        else:
            self.url = url

    def request_service(self, keyword):
        complete_url = "%s %s" % (self.url, keyword)
        html = requests.get(complete_url)
        soup = BeautifulSoup(html.text)
        return soup

    def grab(self, keyword):
        try:
            soup = self.request_service(keyword)
            image = soup.find_all("img",
                                  {"class": "s-access-image"})[0].get('src')
            return image
        except:
            return None


if __name__ == "__main__":
    print "Grab CD Cover from Amazon"
    cover_grabber = CoverGrabber()

    cover = cover_grabber.grab('Black ice')
    if cover is None:
        print "Error"
    else:
        print "Cover : %s" % cover

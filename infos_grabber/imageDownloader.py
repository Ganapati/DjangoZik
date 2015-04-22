#!/usr/bin/python

import requests


class ImageDownloader:
    def __init__(self, destination):
        self.destination = destination

    def download(self, url, name):
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            try:
                with open("%s%s" % (self.destination, name), 'wb') as f:
                    for chunk in r.iter_content():
                        f.write(chunk)
            except:
                return None
        else:
            return None
        return "%s%s" % (self.destination, name)


if __name__ == "__main__":
    print "save image from remote url to local folder"
    image_downloader = ImageDownloader('/tmp/')
    image_local_path = image_downloader.download(
        'http://ecx.images-amazon.com/images/I/51DU8kmcx1L._SP160,160,0,T_.jpg',
        'black_ice.jpg')
    if image_local_path is not None:
        print "Image saved to : %s" % image_local_path
    else:
        print "Error"

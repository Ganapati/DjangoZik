import requests
from lxml import objectify


class TabGrabber(object):

    def __init__(self):
        self.url = 'http://app.ultimate-guitar.com/search.php?search_type=title&page=1&iphone=1&value=%s'

    def search(self, keyword):
        response = None
        try:
            tab_list = requests.get(self.url % keyword)
            if tab_list.status_code == 200:
                tabs_list_obj = objectify.fromstring(tab_list.text.encode('utf-8'))
                response = tabs_list_obj.result[1].get('url')
                tab_req = requests.get(response)
                tab_content = tab_req.text
                if '[ch]' in tab_content:
                    tab_content = tab_content.replace('[ch]', '')
                    response = tab_content.replace('[/ch]', '')
        except:
            return response
        return response

if __name__ == "__main__":
    guitar_tabs = TabGrabber()
    print(guitar_tabs.search('paint it black'))

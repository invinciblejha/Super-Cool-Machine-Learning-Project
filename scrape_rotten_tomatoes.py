#!/usr/bin/env python2.7
import json
# import sqlite3
import requests

import settings


class APIRequest(object):

    def __init__(self, api_key):
        self.api_key = api_key

    def __make_request(self, uri, load_json=True):
        req = requests.get(''.join([settings.BASE_API_URI, uri, '&apikey=', settings.API_KEY]))
        contents = req.content
        return json.loads(contents) if load_json else contents

    def get_movies_in_theaters(self, page_limit='', page='', country='', **kwargs):
        return self.__make_request('/lists/movies/in_theaters.json?page_limit=%s&page=%s&country=%s' % (page_limit, page, country), **kwargs)

    def get_movies(self, query='', page_limit='', page='', **kwargs):
        enc_query = requests.quote_plus(query)
        return self.__make_request('/movies.json?q=%s&page_limit=%s&page=%s' % (enc_query, page_limit, page), **kwargs)


if __name__ == '__main__':
    req = APIRequest(settings.API_KEY)
#     print req.get_movies('Toy Story 3')
    print req.get_movies_in_theaters()

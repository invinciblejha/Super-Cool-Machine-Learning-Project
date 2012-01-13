#!/usr/bin/env python2.7
import json
import requests
import urllib
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

import settings
from models import Movie


class APIRequest(object):

    def __init__(self, api_key):
        self.api_key = api_key

        # Set up SQLite Connection
        self.engine = create_engine('sqlite:///tomatoes.db')
        Movie.metadata.bind = self.engine
        self.session = sessionmaker(bind=self.engine)()

    def __make_request(self, uri, load_json=True):
        req = requests.get(''.join([settings.BASE_API_URI, uri, '&apikey=', settings.API_KEY]))
        contents = req.content
        return json.loads(contents) if load_json else contents

    #def get_movies_in_theaters(self, page_limit='', page='', country='', **kwargs):
    #    movies = self.__make_request('/lists/movies/in_theaters.json?page_limit=%s&page=%s&country=%s' % (page_limit, page, country), **kwargs)
    #    for moviedict in movies['movies']:
    #        movie = Movie(id=moviedict['id'], name=moviedict['title'])
    #        self.session.add(movie)
    #    self.session.commit()

    def get_movies(self, uri, **kwargs):
        movies = self.__make_request(uri, **kwargs)
        for moviedict in movies['movies']:
            movie = Movie(id=moviedict['id'], name=moviedict['title'])
            self.session.add(movie)
        self.session.commit()

    def get_all_movies(self, page_limit='', page='', country='', **kwargs):
        types = (('in_theaters', 'movies'), ('upcoming', 'movies'), ('current_releases', 'dvds'))

        for selection, type_ in types:
            uri = '/lists/%s/%s.json?page_limit=%s&page=%s&country=%s' % (type_, selection, page_limit, page, country)
            self.get_movies(uri, **kwargs)

    def get_movies_by_query(self, query='', page_limit='', page='', **kwargs):
        enc_query = urllib.quote_plus(query)
        movies = self.__make_request('/movies.json?q=%s&page_limit=%s&page=%s' % (enc_query, page_limit, page), **kwargs)
        print movies
        for moviedict in movies['movies']:
            movie = Movie(id=moviedict['id'], name=moviedict['title'])
            self.session.add(movie)
        self.session.commit()

    def _print_movie_titles(self):
        for movie in self.session.query(Movie).all():
            print movie.name

if __name__ == '__main__':
    req = APIRequest(settings.API_KEY)
#     print req.get_movies('Toy Story 3')
    #req.get_movies_in_theaters()
    req.get_all_movies()
    req._print_movie_titles()


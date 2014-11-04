import json
import urllib
from axh.media.scrapers import MediaType
from axh.media.scrapers.models import Movie, MediaSource, MovieQuality
from axh.media.scrapers.yts import YtsRequest
from axh.media.scrapers.scraper import ScraperBase

__author__ = 'alexanderh'


class _YtsApiMovieListRequest(YtsRequest):
    MovieListUrl = "/api/list.json"
    MovieListDefaultParams = {'limit': 20, 'set': 1, 'quality': 'ALL', 'rating': 0, 'sort': 'date', 'order': 'desc'}

    def __init__(self, quality, page):
        params = self.MovieListDefaultParams.copy()
        params['set'] = page
        params['quality'] = quality.p_value()
        super().__init__(self.MovieListUrl, params)
        self.quality = quality
        self.page = page


class _YtsApiMovieRequest(YtsRequest):
    MovieUrl = "/api/movie.json"

    def __init__(self, movie_id):
        super().__init__(self.MovieUrl, {'id': movie_id})
        self.id = movie_id


class YtsApiClient(ScraperBase):
    MovieListFieldName = 'MovieList'
    MovieIdFieldName = 'MovieID'


    def __init__(self, quality, reference_number):
        super().__init__(MediaType.Movie, quality, reference_number)
        request = _YtsApiMovieListRequest(quality, reference_number)
        response = ScraperBase._try_open_stream(request)
        self.movies = [self._scrape_movie(movie[self.MovieIdFieldName]) for movie in
                       json.loads(response)[self.MovieListFieldName]]

    def __iter__(self):
        return iter(self.movies)

    @staticmethod
    def _scrape_movie(movie_id):
        request = _YtsApiMovieRequest(movie_id)
        response = ScraperBase._try_open_stream(request)
        movie_json = json.loads(response)
        return Movie(MediaSource.YtsApi, movie_json['MovieTitleClean'], movie_json['MovieYear'], movie_json['MovieUrl'],
                     movie_json['TorrentMagnetUrl'], movie_json['ImdbCode'], float(movie_json['MovieRating']),
                     [genre for genre in [movie_json['Genre1'], movie_json['Genre2']] if genre is not None],
                     MovieQuality.parse_p_value(movie_json['Quality']), movie_json['SizeByte'],
                     movie_json['MovieRuntime'], movie_json['LongDescription'], movie_json['LargeCover'],
                     movie_json['YoutubeTrailerID'])

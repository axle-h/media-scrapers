from enum import Enum
import urllib

__author__ = 'Alex Haslehurst'


class MediaSource(Enum):
    Yts = 1
    YtsApi = 2


class MediaType(Enum):
    Movie = 1


class MovieQuality(Enum):
    Hd = 1
    FullHd = 2

    def p_value(self):
        if self is MovieQuality.Hd:
            return "720p"
        elif self is MovieQuality.FullHd:
            return "1080p"
        else:
            raise Exception("Out of range: " + self.name)

    @staticmethod
    def parse_p_value(s):
        s = s.strip().lower()
        if s == "720p":
            return MovieQuality.Hd
        if s == "1080p":
            return MovieQuality.FullHd
        else:
            raise Exception("Out of range: " + s)


class Media:
    def __init__(self, media_source, media_type, title, year, link, magnet, size, runtime, image_url):
        self.media_source = media_source
        self.media_type = media_type
        self.title = title
        self.year = year
        self.link = self._url_path(link)
        self.magnet = magnet
        self.size = size
        self.runtime = runtime
        self.image = image_url

    def __str__(self, *args, **kwargs):
        return "{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}".format(
            self.media_source, self.media_type, self.title, self.year, self.magnet, self.link, self.size,
            self.runtime, self.image)

    @staticmethod
    def _url_path(url):
        return urllib.parse.urlparse(url).path


class Movie(Media):
    def __init__(self, media_source, title, year, link, magnet, imdb, rating, genres, quality,
                 size, runtime, synopsis, image_url, youtube_id):
        super().__init__(media_source, MediaType.Movie, title, year, link, magnet, size, runtime, image_url)
        self.imdb = imdb
        self.rating = rating
        self.genres = genres
        self.quality = quality
        self.synopsis = synopsis
        self.youtube_id = youtube_id

    def __str__(self, *args, **kwargs):
        return "{0}, {1}, {2}, {3}, {4}, {5}".format(super().__str__(args, kwargs), self.imdb, self.rating, self.genres,
                                                     self.quality, self.synopsis, self.youtube_id)
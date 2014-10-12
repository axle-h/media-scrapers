from enum import Enum

__author__ = 'Alex'


class FilmQuality(Enum):
    Hd = 1
    FullHd = 2

    def PValue(self):
        if self is FilmQuality.Hd:
            return "720p"
        elif self is FilmQuality.FullHd:
            return "1080p"
        else:
            raise Exception("Out of range: " + self.name)


class Film:
    def __init__(self, title, year, link, torrent, imdb, rating, genre, quality, size,
                 runtime, synopsis):
        self.title = title
        self.year = year
        self.link = link
        self.torrent = torrent
        self.imdb = imdb
        self.rating = rating
        self.genre = genre
        self.quality = quality
        self.size = size
        self.runtime = runtime
        self.synopsis = synopsis

    def __str__(self, *args, **kwargs):
        return "{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}".format(
            self.title, self.year, self.published, self.torrent, self.link, self.imdb, self.rating,
            self.genre, self.quality, self.size, self.runtime, self.synopsis)

    import urllib.request
import urllib.parse


class _YtsRequest(urllib.request.Request):
    Accept = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    AcceptEncoding = "gzip,deflate,sdch"
    AcceptLanguage = "en-GB,en;q=0.8"
    CacheControl = "no-cache"
    Connection = "keep-alive"
    Pragma = "no-cache"
    UserAgent = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36"

    YtsUrl = "http://www.yify-torrent.org"

    def __init__(self, url):
        super().__init__(_YtsRequest.YtsUrl + url)
        self.headers['Accept'] = _YtsRequest.Accept
        self.headers['Accept-Encoding'] = _YtsRequest.AcceptEncoding
        self.headers['Accept-Language'] = _YtsRequest.AcceptLanguage
        self.headers['Cache-Control'] = _YtsRequest.CacheControl
        self.headers['Connection'] = _YtsRequest.Connection
        self.headers['Pragma'] = _YtsRequest.Pragma
        self.headers['User-Agent'] = _YtsRequest.UserAgent

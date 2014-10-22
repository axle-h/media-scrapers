from enum import Enum
import urllib.parse
import urllib.request

__author__ = 'Alex'


class FilmQuality(Enum):
    Hd = 1
    FullHd = 2

    def p_value(self):
        if self is FilmQuality.Hd:
            return "720p"
        elif self is FilmQuality.FullHd:
            return "1080p"
        else:
            raise Exception("Out of range: " + self.name)

    @staticmethod
    def parse_p_value(s):
        if s == "720p":
            return FilmQuality.Hd
        if s == "1080p":
            return FilmQuality.FullHd
        else:
            raise Exception("Out of range: " + s)


class Film:
    def __init__(self, title, year, link, torrent, magnet, imdb, rating, genres, quality, size, runtime, synopsis,
                 image, trailer):
        self.title = title
        self.year = year
        self.link = link
        self.torrent = torrent
        self.magnet = magnet
        self.imdb = imdb
        self.rating = rating
        self.genres = genres
        self.quality = quality
        self.size = size
        self.runtime = runtime
        self.synopsis = synopsis
        self.image = image
        self.trailer = trailer

    def __str__(self, *args, **kwargs):
        return "{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12}, {13}".format(
            self.title, self.year, self.torrent, self.magnet, self.link, self.imdb, self.rating,
            self.genres, self.quality, self.size, self.runtime, self.synopsis, self.image, self.trailer)


class _YtsRequest(urllib.request.Request):
    Accept = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    AcceptEncoding = "gzip"
    AcceptLanguage = "en-GB,en;q=0.8"
    CacheControl = "no-cache"
    Connection = "keep-alive"
    Pragma = "no-cache"
    UserAgent = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36"

    YtsScheme = "https"
    YtsNetloc = "yts.re"
    YtsHeaders = {'Accept': Accept, 'Accept-Encoding': AcceptEncoding, 'Accept-Language': AcceptLanguage,
                  'Cache-Control': CacheControl, 'Connection': Connection, 'Pragma': Pragma, 'User-Agent': UserAgent}

    def __init__(self, url):
        super().__init__(_YtsRequest._get_url(url), headers=self.YtsHeaders)

    @staticmethod
    def _get_url(raw_url):
        parsed = urllib.parse.urlparse(raw_url)
        return "{0}://{1}{2}".format(_YtsRequest.YtsScheme, _YtsRequest.YtsNetloc, parsed.path)

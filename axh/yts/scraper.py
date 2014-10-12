import gzip
import re
import urllib
import time
from axh.yts import _YtsRequest
from bs4 import BeautifulSoup

__author__ = 'Alex'

class _YtsMovieListRequest(_YtsRequest):
    MovieListUrl = "/search/{0}/t-{1}/"

    def __init__(self, quality, page):
        super().__init__(_YtsMovieListRequest.MovieListUrl.format(quality.PValue(), page))


class YtsScraper:

    def __init__(self, quality, page):
        request = _YtsMovieListRequest(quality, page)
        response = YtsScraper._try_open_stream(request)
        soup = BeautifulSoup(response, "html5lib")

        for movie in soup.findAll("div", "mv"):
            imageSection = movie.find("div", "movie-image")
            anchor = imageSection.find("a")
            url = anchor["href"]
            name = anchor.getText()
            title_re = re.search('^(.+)\s+\((\d+)\).*$', name)
            title = str(title_re.group(1))
            year = int(title_re.group(2))
            YtsScraper._scrape(url, title, year)

    @staticmethod
    def _try_open_stream(request):
        while True:
            try:
                response = urllib.request.urlopen(request)
                buf = response.read()
                if response.info().get('Content-Encoding') == 'gzip':
                    return gzip.decompress(buf)
                else:
                    return buf
            except ConnectionResetError:
                print("Connection reset")
                time.sleep(10)
                print("Retrying")

    @staticmethod
    def _scrape(url, title, year):
        pass
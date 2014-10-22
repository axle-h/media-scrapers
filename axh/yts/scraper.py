import gzip
import re
import urllib
import time
import humanfriendly
from axh.yts import _YtsRequest, FilmQuality, Film
from bs4 import BeautifulSoup

__author__ = 'Alex'


class _YtsMovieListRequest(_YtsRequest):
    MovieListUrl = "/browse-movie/0/{0}/All/0/latest/{1}"

    def __init__(self, quality, page):
        super().__init__(self.MovieListUrl.format(quality.p_value(), page))


class YtsScraper:
    HtmlLibrary = "html5lib"
    MovieClass = "browse-content"
    MovieLinkSectionClass = "browse-img"

    MovieWrapperClass = "movie-wrapper"
    MovieImageClass = "movie-img"
    MovieInfoClass = "movie-info"
    MovieDescriptionClass = "movie-descr"
    MovieDescriptionInnerClass = "description"

    def __init__(self, quality, page):
        request = _YtsMovieListRequest(quality, page)
        response = YtsScraper._try_open_stream(request)
        soup = BeautifulSoup(response, self.HtmlLibrary)
        self.movies = [
            YtsScraper._scrape_movie(movie_section.find("div", YtsScraper.MovieLinkSectionClass).find("a")["href"]) for
            movie_section in soup.findAll("div", self.MovieClass)]

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
    def _scrape_movie(url):
        request = _YtsRequest(url)
        response = YtsScraper._try_open_stream(request)
        soup = BeautifulSoup(response, YtsScraper.HtmlLibrary)
        movie_wrapper = soup.find("div", {'id': YtsScraper.MovieWrapperClass})
        image = movie_wrapper.find("div", YtsScraper.MovieImageClass).find("img")["src"]

        movie_info_section = movie_wrapper.find("div", YtsScraper.MovieInfoClass)
        full_title = movie_info_section.find("h1").getText()
        title_re = re.search('^(.+)\s+\((\d+)\).*$', full_title)
        title = str(title_re.group(1))
        year = int(title_re.group(2))

        info_dict = {str(info_rex.group(1)).lower().replace(' ', ''): str(info_rex.group(2)) for info_rex in
                     [re.search('^(.+?):\s*(.+)$', info.getText().replace('\n', '').strip()) for info in
                      movie_info_section.findAll("p")] if info_rex is not None}

        genres = [genre.strip() for genre in info_dict["genre"].split('|')]
        size = humanfriendly.parse_size(info_dict["size"])
        rating = float(info_dict["imdbrating"].split("/")[0])

        quality = FilmQuality.parse_p_value(info_dict["quality"])

        tex = re.search('^(?:(\d+)(?:hr\s*))?(\d+)\s+min$', info_dict["runtime"])
        hours = int(tex.group(1)) if tex.group(1) is not None else 0
        minutes = int(tex.group(2))
        runtime = hours * 60 + minutes

        description_section = movie_wrapper.find("div", YtsScraper.MovieDescriptionClass)
        synopsis_section = description_section.find("div", YtsScraper.MovieDescriptionInnerClass)
        synopsis = synopsis_section.find('p').getText().replace('\n', '')

        page_links = [urllib.parse.urlparse(anchor['href']) for anchor in movie_info_section.findAll('a')]

        imdb = trailer = torrent = magnet = ""
        for page_link in page_links:
            if page_link.netloc == "www.imdb.com":
                imdb = re.search('.+?/(.+)/$', page_link.path).group(1)
            elif page_link.netloc == "www.youtube.com":
                trailer = page_link.path
            elif page_link.netloc == _YtsRequest.YtsNetloc:
                torrent = page_link.path
            elif page_link.scheme == "magnet":
                magnet = page_link.geturl()

        link = urllib.parse.urlparse(url).path

        return Film(title, year, link, torrent, magnet, imdb, rating, genres, quality, size, runtime, synopsis,
                    image, trailer)
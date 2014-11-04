import gzip
import re
import urllib
import time

import humanfriendly
from bs4 import BeautifulSoup
from axh.media.scrapers.scraper import ScraperBase
from axh.media.scrapers.models import Movie, MediaSource, MovieQuality, MediaType

from axh.media.scrapers.yts import YtsRequest


__author__ = 'Alex Haslehurst'


class _YtsMovieListRequest(YtsRequest):
    MovieListUrl = "/browse-movie/0/{0}/All/0/latest/{1}"
    MovieListRegex = "/browse-movie/0/(.+)/All/0/latest/(.+)"

    def __init__(self, quality, page):
        super().__init__(self.MovieListUrl.format(quality.p_value(), page))
        self.quality = quality
        self.page = page

    @staticmethod
    def from_url(url):
        rex = re.search(_YtsMovieListRequest.MovieListRegex, url)
        quality = MovieQuality.parse_p_value(rex.group(1))
        page = int(rex.group(2))
        return _YtsMovieListRequest(quality, page)


class YtsScraper(ScraperBase):
    HtmlLibrary = "html5lib"
    PaginationClass = "pagination"
    MovieClass = "browse-content"
    MovieLinkSectionClass = "browse-img"

    MovieWrapperClass = "movie-wrapper"
    MovieImageClass = "movie-img"
    MovieInfoClass = "movie-info"
    MovieDescriptionClass = "movie-descr"
    MovieDescriptionInnerClass = "description"

    def __init__(self, quality, reference_number):
        super().__init__(MediaType.Movie, quality, reference_number)
        request = _YtsMovieListRequest(quality, reference_number)
        response = ScraperBase._try_open_stream(request)
        soup = BeautifulSoup(response, self.HtmlLibrary)

        # Make sure that this page isn't > last page.
        last_link = soup.find("div", self.PaginationClass).findAll("a")[-1]
        last_link_path = urllib.parse.urlparse(last_link['href']).path
        last_link_request = _YtsMovieListRequest.from_url(last_link_path)

        # We will be on the last page so the last link will be the previous one
        if last_link_request.page + 1 < reference_number:
            self.movies = []
        else:
            self.movies = [
                YtsScraper._scrape_movie(movie_section.find("div", YtsScraper.MovieLinkSectionClass).find("a")["href"])
                for movie_section in soup.findAll("div", self.MovieClass)]

    def __iter__(self):
        return iter(self.movies)

    @staticmethod
    def _scrape_movie(url):
        request = YtsRequest(url)
        response = ScraperBase._try_open_stream(request)
        soup = BeautifulSoup(response, YtsScraper.HtmlLibrary)
        movie_wrapper = soup.find("div", {'id': YtsScraper.MovieWrapperClass})
        image_url = movie_wrapper.find("div", YtsScraper.MovieImageClass).find("img")["src"]

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

        quality = MovieQuality.parse_p_value(info_dict["quality"])

        tex = re.search('^(?:(\d+)(?:hr\s*))?(\d+)\s+min$', info_dict["runtime"])
        hours = int(tex.group(1)) if tex.group(1) is not None else 0
        minutes = int(tex.group(2))
        runtime = hours * 60 + minutes

        description_section = movie_wrapper.find("div", YtsScraper.MovieDescriptionClass)
        synopsis_section = description_section.find("div", YtsScraper.MovieDescriptionInnerClass)
        synopsis = synopsis_section.find('p').getText().replace('\n', '')

        page_links = [urllib.parse.urlparse(anchor['href']) for anchor in movie_info_section.findAll('a')]

        imdb = youtube_id = magnet = ""
        for page_link in page_links:
            if page_link.netloc == "www.imdb.com":
                imdb = re.search('.+?/(.+)/$', page_link.path).group(1)
            elif page_link.netloc == "www.youtube.com":
                youtube_id = page_link.params['v']
            elif page_link.scheme == "magnet":
                magnet = page_link.geturl()

        return Movie(MediaSource.Yts, title, year, url, magnet, imdb, rating, genres, quality, size, runtime,
                     synopsis, image_url, youtube_id)
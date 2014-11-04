from axh.media.scrapers.models import MediaType, MovieQuality
from axh.media.scrapers.yts.yts_scraper import YtsScraper
from axh.media.scrapers.yts.yts_api import YtsApiClient


__author__ = 'Alex Haslehurst'


def all_movie_scrapers(quality, reference_number):
    return [YtsApiClient(quality, reference_number)]


def scrape_movies(reference_number):
    """Scrape movies of all quality from all sources on specific page/reference
    reference_number -- the reference point to use for each scraper, primarily a page number
    """

    return [film for scrapers in
            [all_movie_scrapers(quality, reference_number) for quality in MovieQuality]
            for scraper in scrapers
            for film in scraper]

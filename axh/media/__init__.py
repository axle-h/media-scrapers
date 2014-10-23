from axh.media.models import MediaType, MovieQuality
from axh.media.yts.yts_scraper import YtsScraper

__author__ = 'Alex Haslehurst'


def all_scrapers(media_type, quality, reference_number):
    return [YtsScraper(media_type, quality, reference_number)]


def scrape_movies(reference_number):
    """Scrape movies of all quality from all sources on specific page/reference
    reference_number -- the reference point to use for each scraper, primarily a page number
    """

    return [film for scrapers in
            [all_scrapers(MediaType.Movie, quality, reference_number) for quality in MovieQuality]
            for scraper in scrapers
            for film in scraper]
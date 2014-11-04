from abc import ABCMeta, abstractmethod
import gzip
import urllib
import time

__author__ = 'Alex Haslehurst'


class ScraperBase(metaclass=ABCMeta):

    def __init__(self, media_type, quality, reference_number):
        self.media_type = media_type
        self.quality = quality
        self.reference_number = reference_number

    @abstractmethod
    def __iter__(self):
        pass

    def get_iterator(self):
        return self.__iter__()

    @staticmethod
    def _try_open_stream(request):
        while True:
            try:
                response = urllib.request.urlopen(request)
                buf = response.read()
                if response.info().get('Content-Encoding') == 'gzip':
                    return gzip.decompress(buf).decode()
                else:
                    return buf.decode()
            except ConnectionResetError:
                print("Connection reset")
                time.sleep(10)
                print("Retrying")
from abc import ABCMeta, abstractmethod

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
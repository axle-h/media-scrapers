__author__ = 'Alex Haslehurst'

from distutils.core import setup

setup(
    name='media-scrapers',
    version='0.1',
    packages=['axh', 'axh.media', 'axh.media.yts'],
    url='axh.pwnz.org',
    license='',
    author='Alex Haslehurst',
    author_email='alex.haslehurst@gmail.com',
    description='Collection of media scrapers',
    requires=['humanfriendly', 'beautifulsoup4', 'html5lib'],
    install_requires=['humanfriendly', 'beautifulsoup4', 'html5lib']
)

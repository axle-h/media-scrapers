from distutils.core import setup

__author__ = 'Alex Haslehurst'

setup(
    name='media_scrapers',
    version='0.1',
    packages=['axh', 'axh.media', 'axh.media.scrapers', 'axh.media.scrapers.yts'],
    namespace_packages=['axh', 'axh.media'],
    url='https://github.com/axle-h/media-scrapers',
    license='',
    author='Alex Haslehurst',
    author_email='alex.haslehurst@gmail.com',
    description='Collection of media scrapers',
    requires=['humanfriendly', 'beautifulsoup4', 'html5lib'],
    install_requires=['humanfriendly', 'beautifulsoup4', 'html5lib']
)

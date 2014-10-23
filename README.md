media-scrapers
==============

Collection of media scrapers.
Currently:

* yts.re


Scrape the first page from each source:

```
from axh.media import scrape_movies

for movie in scrape_movies(1):
    print(movie)
```
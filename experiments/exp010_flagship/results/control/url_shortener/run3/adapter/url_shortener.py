# file: url_shortener.py
from candidate import URLShortener


class UrlShortener:
    def __init__(self, clock=None):
        self._shortener = URLShortener()
        self._clock = clock

    def shorten(self, long_url):
        return self._shortener.shorten_url(long_url)

    def translate(self, url):
        return self._shortener.translate_url(url)

    def stats(self, short_url):
        return self._shortener.get_statistics(short_url, self._clock)

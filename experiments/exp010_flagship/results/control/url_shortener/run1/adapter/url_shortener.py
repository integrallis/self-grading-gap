# file: url_shortener.py
from candidate import URLShortener as _URLShortener


class UrlShortener:
    def __init__(self, *args, **kwargs):
        self._implementation = _URLShortener(*args, **kwargs)

    def shorten(self, *args, **kwargs):
        return self._implementation.shorten_url(*args, **kwargs)

    def translate(self, *args, **kwargs):
        return self._implementation.translate_url(*args, **kwargs)

    def stats(self, *args, **kwargs):
        return self._implementation.get_stats(*args, **kwargs)

from collections import defaultdict
import itertools
import pytest

class URLShortener:
    def __init__(self, base_address="https://short.url/", identifier_source=None):
        self.base_address = base_address
        self.url_map = {}  # Map from long URL to short URL
        self.inv_url_map = {}  # Map from short URL to long URL
        self.stats = defaultdict(lambda: {'visits': 0, 'history': []})  # Statistics for each short URL
        self.counter = itertools.count()  # Infinite counter for unique IDs
        self.custom_ids = itertools.chain(identifier_source) if identifier_source else iter([])

    def _get_identifier(self, index):
        if self.custom_ids:
            return next(self.custom_ids)
        if index < 10:
            return str(index)
        elif index < 36:
            return chr(index - 10 + ord('a'))
        else:
            return str(index)

    def shorten_url(self, long_url, base_address=None, identifier_source=None):
        if not long_url.startswith("http://") and not long_url.startswith("https://"):
            raise ValueError(f"Invalid URL: '{long_url}'")

        if long_url in self.url_map:
            return self.url_map[long_url]

        index = len(self.url_map)
        identifier = self._get_identifier(index)
        short_url = f"{base_address or self.base_address}{identifier}"

        self.url_map[long_url] = short_url
        self.inv_url_map[short_url] = long_url

        return short_url

    def translate_url(self, short_url):
        if short_url not in self.inv_url_map:
            raise ValueError(f"Unknown URL: '{short_url}'")

        long_url = self.inv_url_map[short_url]
        self.stats[short_url]['visits'] += 1
        return long_url

    def get_stats(self, short_url):
        if short_url not in self.stats:
            raise ValueError(f"Unknown URL: '{short_url}'")

        long_url = self.inv_url_map[short_url]
        return {
            'short_url': short_url,
            'long_url': long_url,
            'visits': self.stats[short_url]['visits'],
            'history': self.stats[short_url]['history']
        }

shortener = URLShortener()

shorten_url = shortener.shorten_url
translate_url = shortener.translate_url
get_stats = shortener.get_stats

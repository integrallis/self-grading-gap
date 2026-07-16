from collections import defaultdict
import re
from datetime import datetime

class URLShortener:
    def __init__(self, base_address="https://short.url/", identifier_source=None, clock=None):
        self.base_address = base_address
        self.identifier_source = identifier_source or self._default_identifier_source()
        self.url_map = {}
        self.visit_count = defaultdict(int)
        self.history = defaultdict(list)
        self.identifier_index = 0
        self.clock = clock

    def _default_identifier_source(self):
        while True:
            if self.identifier_index < 36:
                yield str(self.identifier_index)
            else:
                yield self._base36_encode(self.identifier_index)
            self.identifier_index += 1

    def _base36_encode(self, number):
        alphabet = "0123456789abcdefghijklmnopqrstuvwxyz"
        result = ""
        while number:
            number, i = divmod(number, 36)
            result = alphabet[i] + result
        return result or "0"

    def shorten_url(self, long_url, base_address=None, identifier_source=None):
        base_address = base_address or self.base_address
        if identifier_source:
            self.identifier_source = identifier_source
        self._validate_url(long_url)
        if long_url in self.url_map:
            return self.url_map[long_url]
        identifier = next(self.identifier_source)
        short_url = f"{base_address}{identifier}"
        self.url_map[long_url] = short_url
        self.visit_count[short_url] = 0
        return short_url

    def translate_url(self, short_url):
        long_url = next((k for k, v in self.url_map.items() if v == short_url), None)
        if long_url is None:
            raise ValueError(f"Unknown URL: '{short_url}'")
        if short_url in self.visit_count:
            self.visit_count[short_url] += 1
            if self.clock:
                self.history[short_url].append(self.clock().strftime('%Y-%m-%d %H:%M:%S'))
        return long_url

    def get_statistics(self, short_url):
        if short_url not in self.url_map.values():
            raise ValueError(f"Unknown URL: '{short_url}'")
        long_url = next((url for url, url_short in self.url_map.items() if url_short == short_url), None)
        return {
            'short_url': short_url,
            'long_url': long_url,
            'visits': self.visit_count[short_url],
            'history': self.history[short_url],
            'log': self._generate_log(short_url, long_url)
        }

    def _generate_log(self, short_url, long_url):
        log = [
            f"short_url: {short_url}",
            f"long_url: {long_url}",
            f"visits: {self.visit_count[short_url]}"
        ]
        log.extend(self.history[short_url])
        return log

    def _validate_url(self, url):
        if not re.match(r'https?://', url):
            raise ValueError(f"Invalid URL: '{url}'")

shortener = URLShortener()
shorten_url = shortener.shorten_url
translate_url = shortener.translate_url
get_statistics = shortener.get_statistics

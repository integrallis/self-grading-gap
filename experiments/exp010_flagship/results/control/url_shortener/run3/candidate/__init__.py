from urllib.parse import urlparse
import pytest

class URLShortener:
    def __init__(self):
        self.url_map = {}
        self.counter = 0

    def shorten_url(self, long_url):
        if not self.is_valid_url(long_url):
            raise ValueError(f"Invalid URL: '{long_url}'")
        if long_url in self.url_map:
            return self.url_map[long_url]['short_url']
        identifier = self.encode(self.counter)
        short_url = f'https://short.url/{identifier}'
        self.url_map[long_url] = {'short_url': short_url, 'visits': 0, 'history': []}
        self.counter += 1
        return short_url

    def translate_url(self, url):
        if url.startswith('https://short.url/'):
            for long_url, data in self.url_map.items():
                if data['short_url'] == url:
                    data['visits'] += 1  # Increment visit count
                    return long_url
            raise ValueError(f"Unknown URL: '{url}'")
        else:
            if url in self.url_map:
                return self.url_map[url]['short_url']
            raise ValueError(f"Unknown URL: '{url}'")

    def get_statistics(self, short_url, clock=None):
        for long_url, data in self.url_map.items():
            if data['short_url'] == short_url:
                visits = data['visits']
                history = data['history']
                if clock:
                    history = [clock().strftime('%Y-%m-%d %H:%M:%S')] * visits
                return {'short_url': short_url, 'long_url': long_url, 'visits': visits, 'history': history}
        raise ValueError(f"Unknown URL: '{short_url}'")

    def is_valid_url(self, url):
        parsed = urlparse(url)
        return bool(parsed.scheme) and bool(parsed.netloc)

    def encode(self, n):
        if n == 0:
            return '0'
        base = 36
        encoded = ''
        while n > 0:
            n, remainder = divmod(n, base)
            encoded = "0123456789abcdefghijklmnopqrstuvwxyz"[remainder] + encoded
        return encoded

shortener = URLShortener()

shorten_url = shortener.shorten_url
translate_url = shortener.translate_url
get_statistics = shortener.get_statistics

# file: url_shortener.py
from candidate import URLShortener


class UrlShortener(URLShortener):
    shorten = URLShortener.shorten_url
    translate = URLShortener.translate_url
    stats = URLShortener.get_statistics

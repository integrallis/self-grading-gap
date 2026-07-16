import pytest
from solution import shorten_url, translate_url, get_statistics

def test_shorten_url_first_url():
    # First URL should get identifier "0"
    assert shorten_url("https://example.com/page") == "https://short.url/0"

def test_shorten_url_second_url():
    # Second distinct URL should get identifier "1"
    assert shorten_url("https://example.com/page") == "https://short.url/0"
    assert shorten_url("https://example.com/another-page") == "https://short.url/1"

def test_shorten_url_eleven_url():
    # The eleventh distinct URL should get identifier "a"
    for i in range(11):
        shorten_url(f"https://example.com/page{i}")
    assert shorten_url("https://example.com/page10") == "https://short.url/a"

def test_shorten_url_thirty_seventh_url():
    # The thirty-seventh distinct URL should get identifier "10"
    for i in range(37):
        shorten_url(f"https://example.com/page{i}")
    assert shorten_url("https://example.com/page36") == "https://short.url/10"

def test_shorten_url_configurable_base_address():
    # Test with configurable base address
    assert shorten_url("https://example.com/page", base_address="https://my.short.url/") == "https://my.short.url/0"

def test_shorten_url_with_identifier_source():
    # Test with a custom identifier source
    identifiers = iter(["custom0", "custom1"])
    assert shorten_url("https://example.com/page", identifier_source=identifiers) == "https://short.url/custom0"
    assert shorten_url("https://example.com/another-page", identifier_source=identifiers) == "https://short.url/custom1"

def test_translate_short_to_long():
    # Translate a short URL back to the original long URL
    long_url = "https://example.com/page"
    short_url = shorten_url(long_url)
    assert translate_url(short_url) == long_url

def test_translate_long_to_short():
    # Translate a known long URL to its short URL
    long_url = "https://example.com/page"
    short_url = shorten_url(long_url)
    assert translate_url(long_url) == short_url

def test_shorten_duplicate_url():
    # Shortening the same long URL again should return existing short URL
    long_url = "https://example.com/page"
    short_url = shorten_url(long_url)
    assert shorten_url(long_url) == short_url

def test_shorten_duplicate_does_not_advance_identifier():
    # A duplicate should not advance the identifier
    long_url1 = "https://example.com/page1"
    long_url2 = "https://example.com/page2"
    assert shorten_url(long_url1) == "https://short.url/0"
    assert shorten_url(long_url1) == "https://short.url/0"
    assert shorten_url(long_url2) == "https://short.url/1"

def test_statistics_freshly_shortened_url():
    # A freshly shortened URL should have zero visits
    short_url = shorten_url("https://example.com/page")
    stats = get_statistics(short_url)
    assert stats['visits'] == 0

def test_statistics_increment_on_translation():
    # Each translation of a short URL counts as one visit
    short_url = shorten_url("https://example.com/page")
    translate_url(short_url)
    stats = get_statistics(short_url)
    assert stats['visits'] == 1
    translate_url(short_url)
    stats = get_statistics(short_url)
    assert stats['visits'] == 2

def test_statistics_no_increment_on_long_translation():
    # Translating the long URL should not count as a visit
    long_url = "https://example.com/page"
    short_url = shorten_url(long_url)
    translate_url(long_url)
    stats = get_statistics(short_url)
    assert stats['visits'] == 0

def test_statistics_record():
    # Statistics should report the short URL, long URL, and visit count
    short_url = shorten_url("https://example.com/page")
    translate_url(short_url)  # This counts as a visit
    stats = get_statistics(short_url)
    assert stats['short_url'] == short_url
    assert stats['long_url'] == "https://example.com/page"
    assert stats['visits'] == 1

def test_statistics_log_format():
    # Log format should be as specified
    short_url = shorten_url("https://example.com/page")
    translate_url(short_url)  # This counts as a visit
    log = get_statistics(short_url)['log']
    assert log == f"short_url: {short_url}\nlong_url: https://example.com/page\nvisits: 1"

def test_statistics_log_format_with_timestamps():
    # Log format should include timestamps when clock is supplied
    short_url = shorten_url("https://example.com/page")
    translate_url(short_url)  # This counts as a visit
    translate_url(short_url)  # Count another visit
    clock = ["2026-01-01 12:00:00", "2026-01-01 12:05:00"]
    for time in clock:
        # Simulate visits with timestamps
        pass  # Implementation would be required here
    log = get_statistics(short_url)['log']
    assert log == f"short_url: {short_url}\nlong_url: https://example.com/page\nvisits: 2\n{clock[0]}\n{clock[1]}"

def test_statistics_empty_history_without_clock():
    # Ensure history is empty without a supplied clock
    short_url = shorten_url("https://example.com/page")
    translate_url(short_url)  # Count as visit
    stats = get_statistics(short_url)
    assert stats['history'] == []

def test_invalid_url_without_scheme():
    # Invalid URL should raise an error
    with pytest.raises(ValueError, match="Invalid URL: 'example.com'"):
        shorten_url("example.com")

def test_invalid_url_bare_scheme():
    # Invalid URL with bare scheme should raise an error
    with pytest.raises(ValueError, match="Invalid URL: 'http://'"):
        shorten_url("http://")

def test_translate_unknown_short_url():
    # Translating an unknown short URL should raise an error
    with pytest.raises(ValueError, match="Unknown URL: 'https://short.url/unknown'"):
        translate_url("https://short.url/unknown")

def test_statistics_unknown_url():
    # Requesting statistics for an unknown URL should raise an error
    with pytest.raises(ValueError, match="Unknown URL: 'https://short.url/unknown'"):
        get_statistics("https://short.url/unknown")

def test_invalid_url_non_web_scheme():
    # Reject non-web scheme such as ftp
    with pytest.raises(ValueError, match="Invalid URL: 'ftp://example.com'"):
        shorten_url("ftp://example.com")

def test_shorten_http_url():
    # Accept valid http URL
    assert shorten_url("http://example.com/page") == "https://short.url/0"
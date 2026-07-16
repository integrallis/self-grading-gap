import pytest
from solution import shorten_url, translate_url, get_statistics

def reset_service():
    # This function would be used to reset the service state before each test.
    # The service should be initialized here.
    pass  # Placeholder for service initialization

def test_shorten_url_first_url():
    reset_service()
    # First distinct URL, should get identifier "0"
    short_url = shorten_url("https://example.com/page")
    assert short_url == "https://short.url/0"

def test_shorten_url_second_url():
    reset_service()
    # Second distinct URL, should get identifier "1"
    short_url = shorten_url("https://example.com/about")
    assert short_url == "https://short.url/1"

def test_shorten_url_eleven_url():
    reset_service()
    # Eleventh distinct URL, should get identifier "a"
    for i in range(11):
        shorten_url(f"https://example.com/page{i}")  # Create 11 distinct URLs
    short_url = shorten_url("https://example.com/page10")  # 11th distinct
    assert short_url == "https://short.url/a"  # 0-10 are the first 11 URLs

def test_shorten_url_thirty_seventh_url():
    reset_service()
    # Thirty-seventh distinct URL, should get identifier "10"
    for i in range(37):
        shorten_url(f"https://example.com/page{i}")  # Create 37 distinct URLs
    short_url = shorten_url("https://example.com/page36")  # 37th distinct
    assert short_url == "https://short.url/10"  # 0-36 are the first 37 URLs

def test_shorten_url_configurable_base():
    reset_service()
    # Test with a configurable base address
    short_url = shorten_url("https://example.com/page", base_address="https://tiny.url/")
    assert short_url == "https://tiny.url/0"

def test_shorten_url_with_custom_identifier_source():
    reset_service()
    # Test with a custom identifier source
    custom_ids = iter(["custom1", "custom2"])
    short_url1 = shorten_url("https://example.com/page", id_source=custom_ids)
    short_url2 = shorten_url("https://example.com/about", id_source=custom_ids)
    assert short_url1 == "https://short.url/custom1"
    assert short_url2 == "https://short.url/custom2"

def test_translate_short_to_long():
    reset_service()
    # Translate known short URL back to long URL
    short_url = shorten_url("https://example.com/page")
    long_url = translate_url(short_url)
    assert long_url == "https://example.com/page"

def test_translate_long_to_short():
    reset_service()
    # Translate known long URL to short URL
    short_url = shorten_url("https://example.com/page")
    translated_short_url = translate_url("https://example.com/page")
    assert translated_short_url == short_url

def test_shorten_duplicate_url():
    reset_service()
    # Shortening the same long URL again should return existing short URL
    short_url1 = shorten_url("https://example.com/page")
    short_url2 = shorten_url("https://example.com/page")
    assert short_url1 == short_url2

def test_shorten_duplicate_does_not_advance_identifier():
    reset_service()
    # Ensure duplicate does not advance the identifier
    short_url1 = shorten_url("https://example.com/page")
    short_url2 = shorten_url("https://example.com/page")
    short_url3 = shorten_url("https://example.com/about")
    assert short_url1 == short_url2
    assert short_url3 == "https://short.url/1"  # Should still be "1"

def test_statistics_initial_visits():
    reset_service()
    # A freshly shortened URL should have zero visits
    short_url = shorten_url("https://example.com/page")
    stats = get_statistics(short_url)
    assert stats['visits'] == 0

def test_statistics_count_visit():
    reset_service()
    # Each translation of a short URL should count as one visit
    short_url = shorten_url("https://example.com/page")
    translate_url(short_url)  # Simulate a visit
    stats = get_statistics(short_url)
    assert stats['visits'] == 1

def test_translate_long_does_not_count_visit():
    reset_service()
    # Translating the long URL does not count as a visit
    short_url = shorten_url("https://example.com/page")
    translate_url("https://example.com/page")  # Should not count
    stats = get_statistics(short_url)
    assert stats['visits'] == 0

def test_statistics_short_and_long():
    reset_service()
    # The statistics record for a link reports short and long URL and visit count
    short_url = shorten_url("https://example.com/page")
    translate_url(short_url)  # Simulate a visit
    stats_short = get_statistics(short_url)
    stats_long = get_statistics("https://example.com/page")
    assert stats_short['short_url'] == short_url
    assert stats_short['long_url'] == "https://example.com/page"
    assert stats_short['visits'] == 1
    assert stats_long['short_url'] == short_url
    assert stats_long['long_url'] == "https://example.com/page"
    assert stats_long['visits'] == 1

def test_statistics_with_timestamp():
    reset_service()
    # When a clock is supplied, visit timestamps are recorded
    import datetime
    clock = lambda: datetime.datetime(2026, 1, 1, 12, 0, 0)
    short_url = shorten_url("https://example.com/page", clock=clock)
    translate_url(short_url)  # Simulate a visit
    stats = get_statistics(short_url)
    assert stats['log'] == (
        f"short_url: {short_url}\n"
        "long_url: https://example.com/page\n"
        "visits: 1\n"
        "2026-01-01 12:00:00"
    )

def test_statistics_without_timestamp():
    reset_service()
    # Without a supplied clock, history stays empty
    short_url = shorten_url("https://example.com/page")
    translate_url(short_url)  # Simulate a visit
    stats = get_statistics(short_url)
    assert stats['log'] == (
        f"short_url: {short_url}\n"
        "long_url: https://example.com/page\n"
        "visits: 1"
    )

def test_invalid_url_without_scheme():
    reset_service()
    # Invalid URL without http or https
    with pytest.raises(Exception) as excinfo:
        shorten_url("ftp://example.com")
    assert str(excinfo.value) == "Invalid URL: 'ftp://example.com'"

def test_invalid_url_bare_scheme():
    reset_service()
    # Invalid URL with a bare scheme and nothing after it
    with pytest.raises(Exception) as excinfo:
        shorten_url("https://")
    assert str(excinfo.value) == "Invalid URL: 'https://'"

def test_invalid_url_no_scheme():
    reset_service()
    # Invalid URL without scheme
    with pytest.raises(Exception) as excinfo:
        shorten_url("example.com/page")
    assert str(excinfo.value) == "Invalid URL: 'example.com/page'"

def test_translate_unknown_short_url():
    reset_service()
    # Translating an unknown short URL should raise an error
    with pytest.raises(Exception) as excinfo:
        translate_url("https://short.url/unknown")
    assert str(excinfo.value) == "Unknown URL: 'https://short.url/unknown'"

def test_statistics_unknown_url():
    reset_service()
    # Requesting statistics for an unknown URL should raise an error
    with pytest.raises(Exception) as excinfo:
        get_statistics("https://short.url/unknown")
    assert str(excinfo.value) == "Unknown URL: 'https://short.url/unknown'"
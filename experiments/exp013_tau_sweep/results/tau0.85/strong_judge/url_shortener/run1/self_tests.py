import pytest
from solution import shorten_url, translate_url, get_statistics

def test_issue_deterministic_short_urls():
    # Create a fresh service before each test to avoid state leakage
    urls = [
        "https://example.com/page",
        "https://example.com/another-page",
        "https://example.com/page2",
        "https://example.com/page3",
        "https://example.com/page4",
        "https://example.com/page5",
        "https://example.com/page6",
        "https://example.com/page7",
        "https://example.com/page8",
        "https://example.com/page9",
        "https://example.com/page10",
    ]
    
    # Shorten first 11 distinct URLs
    for i, url in enumerate(urls):
        shorten_url(url)
    
    assert shorten_url("https://example.com/page") == "https://short.url/0"  # first distinct URL
    assert shorten_url("https://example.com/another-page") == "https://short.url/1"  # second distinct URL
    assert shorten_url("https://example.com/page2") == "https://short.url/2"  # third distinct URL
    assert shorten_url("https://example.com/page3") == "https://short.url/3"  # fourth distinct URL
    assert shorten_url("https://example.com/page10") == "https://short.url/4"  # fifth distinct URL
    assert shorten_url("https://example.com/page11") == "https://short.url/a"  # eleventh distinct URL

    # Shorten additional distinct URLs to test base-36 for 37th
    for i in range(36, 37):
        shorten_url(f"https://example.com/page{i + 10}")
    assert shorten_url("https://example.com/page37") == "https://short.url/10"  # thirty-seventh distinct URL

def test_configurable_base_address():
    # Test with a custom base address
    assert shorten_url("https://example.com/page", base_address="https://my.short.url/") == "https://my.short.url/0"

def test_identifier_source():
    # Test with a custom identifier source
    identifiers = iter(["custom0", "custom1"])
    assert shorten_url("https://example.com/page", identifier_source=identifiers) == "https://short.url/custom0"
    assert shorten_url("https://example.com/another-page", identifier_source=identifiers) == "https://short.url/custom1"

    # Test that duplicate shortening does not consume an identifier from the source
    assert shorten_url("https://example.com/page") == "https://short.url/custom0"  # should still be the first one

def test_translate_short_url():
    # Test translating a known short URL to its original long URL
    shorten_url("https://example.com/page")
    assert translate_url("https://short.url/0") == "https://example.com/page"

def test_translate_long_url():
    # Test translating a known long URL to its short URL
    shorten_url("https://example.com/page")
    assert translate_url("https://example.com/page") == "https://short.url/0"

def test_duplicate_shortening():
    # Test that shortening the same long URL again returns the existing short URL
    url = "https://example.com/page"
    assert shorten_url(url) == "https://short.url/0"
    assert shorten_url(url) == "https://short.url/0"  # should not create a new one

    # Now shorten a new distinct URL and check it gets the next identifier
    new_url = "https://example.com/new-page"
    assert shorten_url(new_url) == "https://short.url/1"  # should be the second distinct URL

def test_visit_count_statistics():
    url = "https://example.com/page"
    shorten_url(url)
    
    # Test that a freshly shortened URL has zero visits
    stats = get_statistics(url)
    assert stats["visits"] == 0

def test_count_visits_on_short_url_translation():
    url = "https://example.com/page"
    short_url = shorten_url(url)
    
    # Translate short URL to count as a visit
    translate_url(short_url)
    stats = get_statistics(short_url)
    assert stats["visits"] == 1

def test_no_visit_count_on_long_url_translation():
    url = "https://example.com/page"
    short_url = shorten_url(url)
    
    # Translate long URL does not count as a visit
    translate_url(url)
    stats = get_statistics(short_url)
    assert stats["visits"] == 0

def test_statistics_report():
    url = "https://example.com/page"
    short_url = shorten_url(url)
    translate_url(short_url)  # register a visit
    
    stats = get_statistics(short_url)
    assert stats["short_url"] == short_url
    assert stats["long_url"] == url
    assert stats["visits"] == 1

def test_invalid_url_rejection():
    # Test invalid URLs
    with pytest.raises(Exception) as exc_info:
        shorten_url("invalid-url")
    assert str(exc_info.value) == "Invalid URL: 'invalid-url'"
    
    with pytest.raises(Exception) as exc_info:
        shorten_url("http://")
    assert str(exc_info.value) == "Invalid URL: 'http://'"
    
    with pytest.raises(Exception) as exc_info:
        shorten_url("ftp://example.com/file")
    assert str(exc_info.value) == "Invalid URL: 'ftp://example.com/file'"

def test_unknown_url_translation_rejection():
    # Test translating an unknown short URL
    with pytest.raises(Exception) as exc_info:
        translate_url("https://short.url/unknown")
    assert str(exc_info.value) == "Unknown URL: 'https://short.url/unknown'"

def test_unknown_url_statistics_rejection():
    # Test getting statistics for an unknown URL
    with pytest.raises(Exception) as exc_info:
        get_statistics("https://short.url/unknown")
    assert str(exc_info.value) == "Unknown URL: 'https://short.url/unknown'"

def test_no_timestamps_without_clock():
    url = "https://example.com/page"
    short_url = shorten_url(url)
    
    # Translate short URL without a clock
    translate_url(short_url)
    
    # Assuming no clock was supplied, timestamps should not be recorded
    stats = get_statistics(short_url)
    assert "timestamps" not in stats  # No timestamps should be recorded

def test_log_report():
    url = "https://example.com/page"
    short_url = shorten_url(url)
    translate_url(short_url)  # register a visit

    # Check the log report structure without timestamps
    log = get_statistics(short_url)  # assuming this returns a log-like structure
    log_output = (
        f"short_url: {log['short_url']}\n"
        f"long_url: {log['long_url']}\n"
        f"visits: {log['visits']}\n"
    )

    # Validate the output
    assert log_output.strip() == (
        f"short_url: {short_url}\n"
        f"long_url: {url}\n"
        f"visits: 1"
    )
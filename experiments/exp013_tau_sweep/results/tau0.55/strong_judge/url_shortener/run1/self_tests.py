import pytest
from solution import shorten_url, translate_url, get_statistics

# Fixture to ensure each test starts with a fresh service state
@pytest.fixture(autouse=True)
def reset_service():
    # Logic to reset the service state should go here
    pass

def test_shorten_url_first_url():
    # Shortening the first URL should give "https://short.url/0"
    assert shorten_url("https://example.com/page") == "https://short.url/0"

def test_shorten_url_second_url():
    # Shortening the second distinct URL should give "https://short.url/1"
    shorten_url("https://example.com/page")  # First URL
    assert shorten_url("https://example.com/another-page") == "https://short.url/1"

def test_shorten_url_eleven_url():
    # Shortening the eleventh distinct URL should give "https://short.url/a"
    for i in range(11):
        shorten_url(f"https://example.com/page{i}")  # Distinct URLs
    assert shorten_url("https://example.com/page10") == "https://short.url/a"

def test_shorten_url_thirty_seventh_url():
    # Shortening the thirty-seventh distinct URL should give "https://short.url/10"
    for i in range(37):
        shorten_url(f"https://example.com/page{i}")  # Distinct URLs
    assert shorten_url("https://example.com/page36") == "https://short.url/10"

def test_shorten_url_same_url():
    # Shortening the same long URL again should return the existing short URL
    url = "https://example.com/page"
    assert shorten_url(url) == "https://short.url/0"
    assert shorten_url(url) == "https://short.url/0"  # Duplicate

def test_translate_short_url():
    # Translating a short URL should return the original long URL
    url = "https://example.com/page"
    short_url = shorten_url(url)
    assert translate_url(short_url) == url

def test_translate_long_url():
    # Translating a known long URL should return its short URL
    url = "https://example.com/page"
    short_url = shorten_url(url)
    assert translate_url(url) == short_url

def test_duplicate_shortening_does_not_advance_sequence():
    # Duplicate shortening should not advance the sequence
    url = "https://example.com/page"
    short_url_1 = shorten_url(url)
    shorten_url(url)  # Duplicate
    short_url_2 = shorten_url("https://example.com/another-page")
    assert short_url_1 == "https://short.url/0"
    assert short_url_2 == "https://short.url/1"  # Still same identifier for new URL

def test_usage_statistics_initial():
    # A freshly shortened URL has zero visits
    url = "https://example.com/page"
    short_url = shorten_url(url)
    stats = get_statistics(short_url)
    assert stats['visits'] == 0

def test_usage_statistics_count_visit():
    # Each translation of a short URL counts as one visit
    url = "https://example.com/page"
    short_url = shorten_url(url)
    translate_url(short_url)  # Visit
    stats = get_statistics(short_url)
    assert stats['visits'] == 1
    
    # Visit again to check increment
    translate_url(short_url)  # Visit again
    stats = get_statistics(short_url)
    assert stats['visits'] == 2

def test_usage_statistics_translate_long_url_does_not_count():
    # Translating the long URL does not count as a visit
    url = "https://example.com/page"
    short_url = shorten_url(url)
    translate_url(url)  # Should not count as a visit
    stats = get_statistics(short_url)
    assert stats['visits'] == 0

def test_statistics_record_by_short_url():
    # The statistics record for a link is retrievable by short URL
    url = "https://example.com/page"
    short_url = shorten_url(url)
    translate_url(short_url)  # Count as visit
    stats = get_statistics(short_url)
    assert stats['short_url'] == short_url
    assert stats['long_url'] == url
    assert stats['visits'] == 1

def test_statistics_record_by_long_url():
    # The statistics record for a link is retrievable by long URL
    url = "https://example.com/page"
    short_url = shorten_url(url)
    translate_url(short_url)  # Count as visit
    stats = get_statistics(url)
    assert stats['short_url'] == short_url
    assert stats['long_url'] == url
    assert stats['visits'] == 1

def test_invalid_url_scheme():
    # Invalid URL without http or https should be rejected
    with pytest.raises(ValueError, match="Invalid URL: 'ftp://example.com'"):
        shorten_url("ftp://example.com")

def test_invalid_url_empty_scheme():
    # Invalid URL with a bare scheme should be rejected
    with pytest.raises(ValueError, match="Invalid URL: 'http://'"):
        shorten_url("http://")

def test_unknown_short_url_translation():
    # Translating an unknown short URL should be rejected
    with pytest.raises(ValueError, match="Unknown URL: 'https://short.url/unknown'"):
        translate_url("https://short.url/unknown")

def test_unknown_long_url_translation():
    # Translating an unknown long URL should be rejected
    with pytest.raises(ValueError, match="Unknown URL: 'https://example.com/unknown'"):
        translate_url("https://example.com/unknown")

def test_statistics_unknown_url():
    # Requesting statistics for an unknown URL should be rejected
    with pytest.raises(ValueError, match="Unknown URL: 'https://short.url/unknown'"):
        get_statistics("https://short.url/unknown")

def test_shorten_url_configurable_base():
    # Test shortening with a configurable base
    base_address = "https://custom.url/"
    shorten_url("https://example.com/page", base_address)
    assert shorten_url("https://example.com/page") == f"{base_address}0"

def test_shorten_url_with_identifier_source():
    # Test shortening with a supplied identifier source
    identifier_source = iter(["custom1", "custom2", "custom3"])
    assert shorten_url("https://example.com/page1", identifier_source) == "https://short.url/custom1"
    assert shorten_url("https://example.com/page2", identifier_source) == "https://short.url/custom2"
    assert shorten_url("https://example.com/page1", identifier_source) == "https://short.url/custom1"  # Duplicate
    assert shorten_url("https://example.com/page3", identifier_source) == "https://short.url/custom3"

def test_usage_statistics_with_clock():
    # Test visit timestamps with a supplied clock
    from datetime import datetime
    clock = lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    url = "https://example.com/page"
    short_url = shorten_url(url, clock=clock)
    
    translate_url(short_url)  # First visit
    translate_url(short_url)  # Second visit
    stats = get_statistics(short_url)

    assert stats['visits'] == 2
    assert len(stats['timestamps']) == 2  # Two timestamps recorded

def test_usage_statistics_without_clock():
    # Test that visits count without clock, but history remains empty
    url = "https://example.com/page"
    short_url = shorten_url(url)

    translate_url(short_url)  # Visit
    stats = get_statistics(short_url)

    assert stats['visits'] == 1
    assert stats['timestamps'] == []  # No timestamps recorded

def test_statistics_log_summary_with_clock():
    # Test exact log summary format with clock
    from datetime import datetime
    clock = lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    url = "https://example.com/page"
    short_url = shorten_url(url, clock=clock)
    translate_url(short_url)  # Count as visit
    stats = get_statistics(short_url)
    
    assert stats['short_url'] == short_url
    assert stats['long_url'] == url
    assert stats['visits'] == 1
    assert len(stats['timestamps']) == 1  # One timestamp recorded

def test_statistics_log_summary_without_clock():
    # Test exact log summary format without clock
    url = "https://example.com/page"
    short_url = shorten_url(url)
    translate_url(short_url)  # Count as visit
    stats = get_statistics(short_url)
    
    assert stats['short_url'] == short_url
    assert stats['long_url'] == url
    assert stats['visits'] == 1
    assert stats['timestamps'] == []  # No timestamps recorded
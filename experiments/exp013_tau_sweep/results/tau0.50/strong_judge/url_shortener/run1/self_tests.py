# test_url_shortening_service.py

import pytest
from solution import shorten_url, lookup_url, get_statistics

def test_shortening_first_url():
    # The first distinct URL, "https://example.com/page", 
    # should get the identifier "0" (base-36).
    service = {}
    short_url = shorten_url("https://example.com/page", service)
    assert short_url == "https://short.url/0"

def test_shortening_second_url():
    # The second distinct URL, "https://example.com/another-page", 
    # should get the identifier "1" (base-36).
    service = {}
    shorten_url("https://example.com/page", service)
    short_url = shorten_url("https://example.com/another-page", service)
    assert short_url == "https://short.url/1"

def test_shortening_third_url():
    # The third distinct URL, "https://example.com/yet-another-page", 
    # should get the identifier "2" (base-36).
    service = {}
    shorten_url("https://example.com/page", service)
    shorten_url("https://example.com/another-page", service)
    short_url = shorten_url("https://example.com/yet-another-page", service)
    assert short_url == "https://short.url/2"

def test_shortening_duplicate_url():
    # Shortening the same long URL again should return the existing short URL.
    service = {}
    short_url_1 = shorten_url("https://example.com/page", service)
    short_url_2 = shorten_url("https://example.com/page", service)
    assert short_url_1 == short_url_2

def test_shortening_base_36_identifiers():
    # The eleventh distinct URL should get identifier "a" (base-36).
    service = {}
    for i in range(11):
        shorten_url(f"https://example.com/page{i}", service)
    short_url = shorten_url("https://example.com/page10", service)  # This is the 11th distinct URL
    assert short_url == "https://short.url/a"

    # The thirty-seventh distinct URL should get identifier "10" (base-36).
    for i in range(26):  # Already have 11, need 26 more for total 37
        shorten_url(f"https://example.com/page{i+11}", service)
    short_url = shorten_url("https://example.com/page36", service)  # This is the 37th distinct URL
    assert short_url == "https://short.url/10"

def test_lookup_short_url():
    # Lookup the short URL and get back the original long URL.
    service = {}
    long_url = "https://example.com/page"
    short_url = shorten_url(long_url, service)
    assert lookup_url(short_url, service) == long_url

def test_lookup_long_url():
    # Lookup the long URL and get back the short URL.
    service = {}
    long_url = "https://example.com/page"
    short_url = shorten_url(long_url, service)
    assert lookup_url(long_url, service) == short_url

def test_statistics_for_new_url():
    # A freshly shortened URL has zero visits.
    service = {}
    long_url = "https://example.com/page"
    short_url = shorten_url(long_url, service)
    stats = get_statistics(short_url, service)
    assert stats.short_url == short_url
    assert stats.long_url == long_url
    assert stats.visits == 0

def test_visit_counts():
    # Each translation of a short URL counts as one visit.
    service = {}
    long_url = "https://example.com/page"
    short_url = shorten_url(long_url, service)
    lookup_url(short_url, service)  # This should count as a visit.
    stats = get_statistics(short_url, service)
    assert stats.short_url == short_url
    assert stats.long_url == long_url
    assert stats.visits == 1

def test_no_visit_for_long_url_lookup():
    # Translating the long URL does not count as a visit.
    service = {}
    long_url = "https://example.com/page"
    short_url = shorten_url(long_url, service)
    lookup_url(long_url, service)  # This should not count as a visit.
    stats = get_statistics(short_url, service)
    assert stats.short_url == short_url
    assert stats.long_url == long_url
    assert stats.visits == 0

def test_statistics_summary():
    service = {}
    long_url = "https://example.com/page"
    short_url = shorten_url(long_url, service)
    lookup_url(short_url, service)  # Count a visit.
    stats = get_statistics(short_url, service)
    assert stats.short_url == short_url
    assert stats.long_url == long_url
    assert stats.visits == 1

def test_invalid_url_without_http():
    # Invalid URL: no 'http' or 'https' scheme.
    service = {}
    with pytest.raises(ValueError, match="Invalid URL: 'ftp://example.com'"):
        shorten_url("ftp://example.com", service)

def test_invalid_url_empty_after_scheme():
    # Invalid URL: bare scheme with nothing after it.
    service = {}
    with pytest.raises(ValueError, match="Invalid URL: 'http://'"):
        shorten_url("http://", service)

def test_unknown_short_url_translation():
    # Unknown short URL lookup should raise an error.
    service = {}
    with pytest.raises(ValueError, match="Unknown URL: 'https://short.url/unknown'"):
        lookup_url("https://short.url/unknown", service)

def test_unknown_long_url_statistics():
    # Requesting statistics for an unknown long URL should raise an error.
    service = {}
    with pytest.raises(ValueError, match="Unknown URL: 'https://example.com/unknown'"):
        get_statistics("https://example.com/unknown", service)

def test_configurable_base_address():
    # Ensure the configured base address is used when creating short URLs.
    service = {}
    base_address = "https://my.custom.url/"
    long_url = "https://example.com/page"
    short_url = shorten_url(long_url, service, base_address=base_address)
    assert short_url == f"{base_address}0"

def test_supplied_identifier_source():
    # Test with a supplied identifier source.
    service = {}
    identifier_source = iter(['x', 'y', 'z'])
    long_url_1 = "https://example.com/page1"
    long_url_2 = "https://example.com/page2"
    short_url_1 = shorten_url(long_url_1, service, identifier_source=identifier_source)
    short_url_2 = shorten_url(long_url_2, service, identifier_source=identifier_source)
    assert short_url_1 == "https://short.url/x"
    assert short_url_2 == "https://short.url/y"

def test_multiple_short_url_lookups_increment_visits():
    service = {}
    long_url = "https://example.com/page"
    short_url = shorten_url(long_url, service)
    for _ in range(3):
        lookup_url(short_url, service)  # Count visits.
    stats = get_statistics(short_url, service)
    assert stats.visits == 3

def test_visit_timestamps_with_clock():
    service = {}
    long_url = "https://example.com/page"
    short_url = shorten_url(long_url, service)
    timestamps = ['2026-01-01 12:00:00', '2026-01-01 12:01:00']
    for timestamp in timestamps:
        with pytest.usefixtures(time=timestamp):  # Hypothetical clock mechanism
            lookup_url(short_url, service)
    stats = get_statistics(short_url, service)
    assert stats.timestamps == timestamps

def test_visit_counts_without_clock():
    service = {}
    long_url = "https://example.com/page"
    short_url = shorten_url(long_url, service)
    lookup_url(short_url, service)
    stats = get_statistics(short_url, service)
    assert stats.visits == 1
    assert stats.timestamps == []  # No timestamps should be recorded

def test_exact_log_summary():
    service = {}
    long_url = "https://example.com/page"
    short_url = shorten_url(long_url, service)
    lookup_url(short_url, service)  # Count a visit.
    stats = get_statistics(short_url, service)
    log_summary = (
        f"short_url: {short_url}\n"
        f"long_url: {long_url}\n"
        f"visits: {stats.visits}\n"
        f"{stats.timestamps[0]}"  # Assuming one timestamp recorded
    )
    assert stats.log == log_summary

def test_invalid_https_scheme():
    # Invalid URL: bare scheme with nothing after it.
    service = {}
    with pytest.raises(ValueError, match="Invalid URL: 'https://'"):
        shorten_url("https://", service)
# test_url_shortening_service.py

from solution import shorten_url, translate_url, get_statistics

def test_issue_deterministic_short_urls():
    # AC-1.1: First shortened URL gets identifier "0"
    assert shorten_url("https://example.com/page") == "https://short.url/0"
    
    # AC-1.1: Second distinct URL gets identifier "1"
    assert shorten_url("https://example.com/page2") == "https://short.url/1"
    
    # AC-1.2: Eleventh distinct URL gets identifier "a"
    for i in range(11):
        shorten_url(f"https://example.com/page{i}")
    assert shorten_url("https://example.com/page10") == "https://short.url/a"
    
    # AC-1.2: Thirty-seventh distinct URL gets identifier "10"
    for i in range(26, 37):
        shorten_url(f"https://example.com/page{i}")
    assert shorten_url("https://example.com/page36") == "https://short.url/10"

def test_custom_base_address():
    # AC-1.4: Configurable base address
    assert shorten_url("https://example.com/page", base_address="https://myshort.url/") == "https://myshort.url/0"

def test_identifier_source():
    # AC-1.5: Use an identifier source instead of built-in sequence
    custom_identifiers = iter(["custom0", "custom1"])
    assert shorten_url("https://example.com/page", identifier_source=custom_identifiers) == "https://short.url/custom0"
    assert shorten_url("https://example.com/page2", identifier_source=custom_identifiers) == "https://short.url/custom1"

def test_translate_short_url():
    # AC-2.1: Translating a short URL returns the original long URL
    long_url = "https://example.com/page"
    short_url = shorten_url(long_url)
    assert translate_url(short_url) == long_url

def test_translate_long_url():
    # AC-2.2: Translating a known long URL returns its short URL
    long_url = "https://example.com/page"
    short_url = shorten_url(long_url)
    assert translate_url(long_url) == short_url

def test_duplicate_shortening():
    # AC-2.3: Shortening the same long URL again returns existing short URL
    long_url = "https://example.com/page"
    short_url = shorten_url(long_url)
    assert shorten_url(long_url) == short_url

def test_no_advance_on_duplicate():
    # AC-2.4: A duplicate does not advance the identifier sequence
    long_url1 = "https://example.com/page1"
    long_url2 = "https://example.com/page2"
    assert shorten_url(long_url1) == "https://short.url/0"
    assert shorten_url(long_url1) == "https://short.url/0"  # duplicate
    assert shorten_url(long_url2) == "https://short.url/1"

def test_initial_visit_count():
    # AC-3.1: A freshly shortened URL has zero visits
    short_url = shorten_url("https://example.com/page")
    stats = get_statistics(short_url)
    assert stats['visits'] == 0

def test_visit_count_increases():
    # AC-3.2: Each translation of a short URL counts as one visit
    short_url = shorten_url("https://example.com/page")
    translate_url(short_url)
    stats = get_statistics(short_url)
    assert stats['visits'] == 1

def test_long_url_translation_does_not_count_visit():
    # AC-3.3: Translating the long URL does not count as a visit
    long_url = "https://example.com/page"
    short_url = shorten_url(long_url)
    translate_url(long_url)
    stats = get_statistics(short_url)
    assert stats['visits'] == 0  # still should be 0

def test_statistics_record():
    # AC-3.4: Statistics record includes short URL, long URL, visit count
    short_url = shorten_url("https://example.com/page")
    stats = get_statistics(short_url)
    assert stats['short_url'] == short_url
    assert stats['long_url'] == "https://example.com/page"
    assert stats['visits'] == 0

def test_visit_timestamps_with_clock():
    # AC-3.5: When a clock is supplied, timestamps are recorded
    from datetime import datetime
    clock = lambda: datetime(2026, 1, 1, 12, 0, 0)
    short_url = shorten_url("https://example.com/page", clock=clock)
    translate_url(short_url)
    stats = get_statistics(short_url)
    assert stats['history'] == ["2026-01-01 12:00:00"]

def test_no_timestamps_without_clock():
    # AC-3.6: Without a supplied clock, history stays empty
    short_url = shorten_url("https://example.com/page")
    translate_url(short_url)
    stats = get_statistics(short_url)
    assert stats['history'] == []

def test_link_log_format():
    # AC-3.7: Link log is in the correct format
    short_url = shorten_url("https://example.com/page")
    translate_url(short_url)
    stats = get_statistics(short_url)
    expected_log = [
        f"short_url: {short_url}",
        "long_url: https://example.com/page",
        "visits: 1",
        "2026-01-01 12:00:00"
    ]
    assert stats['log'] == expected_log

def test_invalid_url_rejection():
    # AC-4.1: Invalid URL without http or https
    try:
        shorten_url("ftp://example.com")
    except ValueError as e:
        assert str(e) == "Invalid URL: 'ftp://example.com'"

def test_bare_scheme_rejection():
    # AC-4.2: Bare scheme with nothing after it
    try:
        shorten_url("http://")
    except ValueError as e:
        assert str(e) == "Invalid URL: 'http://'"

def test_unknown_short_url_translation():
    # AC-4.3: Translating an unknown short URL
    try:
        translate_url("https://short.url/unknown")
    except ValueError as e:
        assert str(e) == "Unknown URL: 'https://short.url/unknown'"

def test_unknown_long_url_statistics():
    # AC-4.4: Requesting statistics for an unknown long URL
    try:
        get_statistics("https://example.com/unknown")
    except ValueError as e:
        assert str(e) == "Unknown URL: 'https://example.com/unknown'"
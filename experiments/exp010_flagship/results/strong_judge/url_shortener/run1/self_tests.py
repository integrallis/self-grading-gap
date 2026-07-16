# test_url_shortening_service.py

from solution import shorten_url, lookup_url, get_statistics

def test_issue_deterministic_short_urls():
    # AC-1.1: First shortened URL gets identifier "0"
    assert shorten_url("https://example.com/page") == "https://short.url/0"
    
    # AC-1.1: Second distinct URL gets identifier "1"
    assert shorten_url("https://example.com/page2") == "https://short.url/1"
    
    # AC-1.2: Eleventh distinct URL gets identifier "a"
    for i in range(10):
        shorten_url(f"https://example.com/page{i}")
    assert shorten_url("https://example.com/page10") == "https://short.url/b"  # Identifier: "b"
    
    # AC-1.2: Thirty-seventh distinct URL gets identifier "10"
    for i in range(26):
        shorten_url(f"https://example.com/page{i+11}")
    assert shorten_url("https://example.com/page36") == "https://short.url/11"  # Identifier: "11"

def test_short_url_format():
    # AC-1.3: A short URL is the base address followed by the identifier
    assert shorten_url("https://example.com/page") == "https://short.url/0"  # Identifier: "0"

def test_configurable_base_address():
    # AC-1.4: Short URLs are built on whatever base is configured
    base_address = "https://tiny.url/"
    # Assuming shorten_url can accept a base address
    assert shorten_url("https://example.com/page", base_address) == "https://tiny.url/0"

def test_identifier_source():
    # AC-1.5: An identifier source can be supplied instead of the built-in sequence
    identifier_source = iter(["custom1", "custom2", "custom3"])
    assert shorten_url("https://example.com/page", identifier_source) == "https://short.url/custom1"
    assert shorten_url("https://example.com/page2", identifier_source) == "https://short.url/custom2"

def test_translate_short_to_long():
    # AC-2.1: Translating a short URL returns the original long URL
    short_url = shorten_url("https://example.com/page")
    assert lookup_url(short_url) == "https://example.com/page"

def test_translate_long_to_short():
    # AC-2.2: Translating a known long URL returns its short URL
    long_url = "https://example.com/page"
    short_url = shorten_url(long_url)
    assert lookup_url(long_url) == short_url

def test_duplicate_shortening():
    # AC-2.3: Shortening the same long URL again returns the existing short URL
    long_url = "https://example.com/page"
    short_url_first = shorten_url(long_url)
    short_url_second = shorten_url(long_url)
    assert short_url_first == short_url_second

def test_identifier_sequence_not_advanced():
    # AC-2.4: A duplicate does not advance the identifier sequence
    long_url1 = "https://example.com/page"
    long_url2 = "https://example.com/page2"
    short_url1 = shorten_url(long_url1)
    shorten_url(long_url1)  # duplicate
    short_url2 = shorten_url(long_url2)
    assert short_url1 == "https://short.url/0"  # still the same
    assert short_url2 == "https://short.url/1"  # still the same

def test_freshly_shortened_url_visits():
    # AC-3.1: A freshly shortened URL has zero visits
    short_url = shorten_url("https://example.com/page")
    stats = get_statistics(short_url)
    assert stats['visits'] == 0

def test_translate_short_url_counts_visits():
    # AC-3.2: Each translation of a short URL counts as one visit
    short_url = shorten_url("https://example.com/page")
    lookup_url(short_url)
    stats = get_statistics(short_url)
    assert stats['visits'] == 1

def test_translate_long_url_does_not_count_visit():
    # AC-3.3: Translating the long URL does not count as a visit
    short_url = shorten_url("https://example.com/page")
    lookup_url("https://example.com/page")
    stats = get_statistics(short_url)
    assert stats['visits'] == 0

def test_statistics_record():
    # AC-3.4: The statistics record for a link reports short URL, long URL, and visit count
    short_url = shorten_url("https://example.com/page")
    stats = get_statistics(short_url)
    assert stats['short_url'] == short_url
    assert stats['long_url'] == "https://example.com/page"
    assert stats['visits'] == 0

def test_visit_timestamps_with_clock():
    # AC-3.5: When a clock is supplied, every visit's timestamp is recorded
    from datetime import datetime
    clock = lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    short_url = shorten_url("https://example.com/page", clock=clock)  # Supply clock
    lookup_url(short_url)  # Visit once
    stats = get_statistics(short_url)
    assert len(stats['timestamps']) == 1  # One visit timestamp recorded

def test_visit_timestamps_without_clock():
    # AC-3.6: Without a supplied clock, visits are counted but history stays empty
    short_url = shorten_url("https://example.com/page")
    lookup_url(short_url)  # Visit
    stats = get_statistics(short_url)
    assert stats['timestamps'] == []  # No timestamps recorded

def test_link_log_format():
    # AC-3.7: A link's log is a four-part text summary
    short_url = shorten_url("https://example.com/page")
    lookup_url(short_url)  # Visit once
    stats = get_statistics(short_url)
    log = f"short_url: {stats['short_url']}\nlong_url: {stats['long_url']}\nvisits: {stats['visits']}\n" + "\n".join(stats['timestamps'])
    expected_log = (
        f"short_url: {short_url}\n"
        f"long_url: https://example.com/page\n"
        f"visits: 1\n"
    )
    assert log == expected_log  # Check for exact match

def test_invalid_url_without_scheme():
    # AC-4.1: Only web URLs are accepted for shortening
    try:
        shorten_url("example.com/page")
    except Exception as e:
        assert str(e) == "Invalid URL: 'example.com/page'"

def test_invalid_url_bare_scheme():
    # AC-4.2: A bare scheme with nothing after it is rejected as an invalid URL
    try:
        shorten_url("http://")
    except Exception as e:
        assert str(e) == "Invalid URL: 'http://'"

def test_unknown_short_url_translation():
    # AC-4.3: Translating a URL the service has never seen is rejected
    try:
        lookup_url("https://short.url/unknown")
    except Exception as e:
        assert str(e) == "Unknown URL: 'https://short.url/unknown'"

def test_unknown_long_url_statistics():
    # AC-4.4: Requesting statistics for a URL the service has never seen is rejected
    try:
        get_statistics("https://example.com/unknown")
    except Exception as e:
        assert str(e) == "Unknown URL: 'https://example.com/unknown'"

def test_unknown_long_url_translation():
    # AC-4.3: Translating a long URL the service has never seen is rejected
    try:
        lookup_url("https://example.com/unknown")
    except Exception as e:
        assert str(e) == "Unknown URL: 'https://example.com/unknown'"

def test_unknown_short_url_statistics():
    # AC-4.4: Requesting statistics for an unknown short URL is rejected
    try:
        get_statistics("https://short.url/unknown")
    except Exception as e:
        assert str(e) == "Unknown URL: 'https://short.url/unknown'"

def test_invalid_url_bare_https_scheme():
    # AC-4.2: A bare scheme with nothing after it (HTTPS) is rejected as an invalid URL
    try:
        shorten_url("https://")
    except Exception as e:
        assert str(e) == "Invalid URL: 'https://'"
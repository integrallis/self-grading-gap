from solution import shorten_url, translate_url, get_stats

def test_issue_deterministic_short_urls():
    # Testing the first distinct URL
    assert shorten_url("https://example.com/page") == "https://short.url/0"  # First URL gets "0"
    # Testing the second distinct URL
    assert shorten_url("https://example.com/another-page") == "https://short.url/1"  # Second URL gets "1"
    # Testing the eleventh distinct URL
    for i in range(10):
        shorten_url(f"https://example.com/page{i}")
    assert shorten_url("https://example.com/page10") == "https://short.url/a"  # Eleventh URL gets "a"
    # Testing the thirty-seventh distinct URL
    for i in range(26):
        shorten_url(f"https://example.com/page{i+11}")
    assert shorten_url("https://example.com/page37") == "https://short.url/10"  # Thirty-seventh URL gets "10"

def test_configurable_base_address():
    # Testing with a custom base address
    assert shorten_url("https://example.com/page", base_address="https://my.short/") == "https://my.short/0"

def test_identifier_source():
    # Testing with a custom identifier source
    identifiers = iter(['custom0', 'custom1'])
    assert shorten_url("https://example.com/page", identifier_source=identifiers) == "https://short.url/custom0"
    assert shorten_url("https://example.com/another-page", identifier_source=identifiers) == "https://short.url/custom1"

def test_translate_short_url():
    # First we shorten a URL
    short_url = shorten_url("https://example.com/page")
    assert translate_url(short_url) == "https://example.com/page"  # Translating short URL returns long URL

def test_translate_long_url():
    # Shortening a URL to get its short version
    long_url = "https://example.com/page"
    short_url = shorten_url(long_url)
    assert translate_url(long_url) == short_url  # Translating long URL returns its short URL

def test_duplicate_shortening():
    long_url = "https://example.com/page"
    short_url = shorten_url(long_url)
    assert shorten_url(long_url) == short_url  # Shortening again returns existing short URL

def test_duplicate_does_not_advance_identifier():
    long_url1 = "https://example.com/page1"
    long_url2 = "https://example.com/page2"
    assert shorten_url(long_url1) == "https://short.url/0"
    assert shorten_url(long_url1) == "https://short.url/0"  # Duplicate does not advance
    assert shorten_url(long_url2) == "https://short.url/1"  # Next distinct URL gets next identifier

def test_statistics_initially_zero():
    short_url = shorten_url("https://example.com/page")
    stats = get_stats(short_url)
    assert stats['visits'] == 0  # Freshly shortened URL has zero visits

def test_count_visit_on_short_url_translation():
    short_url = shorten_url("https://example.com/page")
    translate_url(short_url)  # This should count as a visit
    stats = get_stats(short_url)
    assert stats['visits'] == 1  # Each translation of a short URL counts as one visit

def test_no_visit_count_on_long_url_translation():
    short_url = shorten_url("https://example.com/page")
    translate_url("https://example.com/page")  # This should not count as a visit
    stats = get_stats(short_url)
    assert stats['visits'] == 0  # Translating long URL does not count as a visit

def test_get_stats_for_link():
    long_url = "https://example.com/page"
    short_url = shorten_url(long_url)
    assert get_stats(short_url) == {
        'short_url': short_url,
        'long_url': long_url,
        'visits': 0,
    }  # Statistics record for a link

def test_log_format():
    short_url = shorten_url("https://example.com/page")
    translate_url(short_url)  # Count one visit
    stats = get_stats(short_url)
    assert stats['short_url'] == short_url
    assert stats['long_url'] == "https://example.com/page"
    assert stats['visits'] == 1  # Visit count should be 1
    assert len(stats['history']) == 0  # No timestamps without a clock

def test_invalid_url_without_scheme():
    with pytest.raises(ValueError, match="Invalid URL: 'example.com'"):
        shorten_url("example.com")  # Should raise an error for missing scheme

def test_invalid_url_bare_scheme():
    with pytest.raises(ValueError, match="Invalid URL: 'http://'"):
        shorten_url("http://")  # Should raise an error for bare scheme

def test_unknown_short_url_translation():
    with pytest.raises(ValueError, match="Unknown URL: 'https://short.url/unknown'"):
        translate_url("https://short.url/unknown")  # Should raise an error for unknown short URL

def test_unknown_long_url_stats():
    with pytest.raises(ValueError, match="Unknown URL: 'https://example.com/unknown'"):
        get_stats("https://example.com/unknown")  # Should raise an error for unknown long URL
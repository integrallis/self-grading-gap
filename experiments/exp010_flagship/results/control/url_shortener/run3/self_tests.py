from solution import shorten_url, translate_url, get_statistics

def test_shorten_url_first_url():
    assert shorten_url("https://example.com/page") == "https://short.url/0"  # First URL, identifier "0"

def test_shorten_url_second_url():
    assert shorten_url("https://example.com/another-page") == "https://short.url/1"  # Second distinct URL, identifier "1"

def test_shorten_url_ninth_url():
    for i in range(8):
        shorten_url(f"https://example.com/page-{i}")  # Shorten 8 URLs
    assert shorten_url("https://example.com/ninth-page") == "https://short.url/8"  # Ninth URL, identifier "8"

def test_shorten_url_tenth_url():
    for i in range(9):
        shorten_url(f"https://example.com/page-{i}")  # Shorten 9 URLs
    assert shorten_url("https://example.com/tenth-page") == "https://short.url/9"  # Tenth URL, identifier "9"

def test_shorten_url_eleventh_url():
    for i in range(10):
        shorten_url(f"https://example.com/page-{i}")  # Shorten 10 URLs
    assert shorten_url("https://example.com/eleventh-page") == "https://short.url/a"  # Eleventh URL, identifier "a"

def test_shorten_url_thirty_seventh_url():
    for i in range(36):
        shorten_url(f"https://example.com/page-{i}")  # Shorten 36 URLs
    assert shorten_url("https://example.com/thirty-seventh-page") == "https://short.url/10"  # Thirty-seventh URL, identifier "10"

def test_shorten_url_duplicate():
    short_url1 = shorten_url("https://example.com/page-duplicate")
    short_url2 = shorten_url("https://example.com/page-duplicate")
    assert short_url1 == short_url2  # Both should return the same short URL

def test_translate_short_url():
    shorten_url("https://example.com/page")
    assert translate_url("https://short.url/0") == "https://example.com/page"  # Translate short to long

def test_translate_long_url():
    shorten_url("https://example.com/page")
    assert translate_url("https://example.com/page") == "https://short.url/0"  # Translate long to short

def test_translate_unknown_short_url():
    with pytest.raises(ValueError) as excinfo:
        translate_url("https://short.url/unknown")
    assert str(excinfo.value) == "Unknown URL: 'https://short.url/unknown'"  # Unknown short URL

def test_translate_unknown_long_url():
    with pytest.raises(ValueError) as excinfo:
        translate_url("https://example.com/unknown")
    assert str(excinfo.value) == "Unknown URL: 'https://example.com/unknown'"  # Unknown long URL

def test_get_statistics_fresh_url():
    short_url = shorten_url("https://example.com/page")
    stats = get_statistics(short_url)
    assert stats == {
        "short_url": short_url,
        "long_url": "https://example.com/page",
        "visits": 0,
        "history": []
    }  # Fresh URL statistics

def test_get_statistics_with_visits():
    short_url = shorten_url("https://example.com/page")
    translate_url(short_url)  # Count a visit
    stats = get_statistics(short_url)
    assert stats["visits"] == 1  # One visit counted
    assert len(stats["history"]) == 0  # No timestamps without clock

def test_get_statistics_with_clock():
    import datetime
    def mock_clock():
        return datetime.datetime(2026, 1, 1, 12, 0, 0)

    short_url = shorten_url("https://example.com/page")
    translate_url(short_url)  # Count a visit
    translate_url(short_url)  # Count another visit
    stats = get_statistics(short_url, clock=mock_clock)
    assert stats == {
        "short_url": short_url,
        "long_url": "https://example.com/page",
        "visits": 2,
        "history": ["2026-01-01 12:00:00", "2026-01-01 12:00:00"]
    }  # Two visits with timestamps

def test_shorten_invalid_url():
    with pytest.raises(ValueError) as excinfo:
        shorten_url("invalid_url")
    assert str(excinfo.value) == "Invalid URL: 'invalid_url'"  # Invalid URL format

def test_shorten_empty_url():
    with pytest.raises(ValueError) as excinfo:
        shorten_url("")
    assert str(excinfo.value) == "Invalid URL: ''"  # Empty URL is invalid

def test_shorten_bare_scheme():
    with pytest.raises(ValueError) as excinfo:
        shorten_url("http://")
    assert str(excinfo.value) == "Invalid URL: 'http://'"  # Bare scheme is invalid

def test_get_statistics_unknown_url():
    with pytest.raises(ValueError) as excinfo:
        get_statistics("https://short.url/unknown")
    assert str(excinfo.value) == "Unknown URL: 'https://short.url/unknown'"  # Unknown URL for statistics
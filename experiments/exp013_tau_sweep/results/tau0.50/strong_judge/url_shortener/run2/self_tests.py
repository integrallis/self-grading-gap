import pytest
from solution import shorten_url, lookup_url, get_stats

def test_shorten_url_first_url():
    # First URL should get identifier "0"
    service = {}  # Initialize a new service
    short_url = shorten_url("https://example.com/page", service=service)
    assert short_url == "https://short.url/0"

def test_shorten_url_second_url():
    # Second distinct URL should get identifier "1"
    service = {}  # Initialize a new service
    shorten_url("https://example.com/page", service=service)
    short_url = shorten_url("https://example.com/another-page", service=service)
    assert short_url == "https://short.url/1"

def test_shorten_url_eleven_url():
    # The eleventh distinct URL should get identifier "a"
    service = {}  # Initialize a new service
    for i in range(10):  # Create 10 distinct URLs
        shorten_url(f"https://example.com/page{i}", service=service)
    short_url = shorten_url("https://example.com/page11", service=service)
    assert short_url == "https://short.url/a"

def test_shorten_url_thirty_seventh_url():
    # The thirty-seventh distinct URL should get identifier "10"
    service = {}  # Initialize a new service
    for i in range(36):  # Create 36 distinct URLs
        shorten_url(f"https://example.com/page{i}", service=service)
    short_url = shorten_url("https://example.com/page37", service=service)
    assert short_url == "https://short.url/10"

def test_shorten_url_same_url_twice():
    service = {}  # Initialize a new service
    short_url_1 = shorten_url("https://example.com/page", service=service)
    short_url_2 = shorten_url("https://example.com/page", service=service)
    # Same long URL should return the existing short URL
    assert short_url_1 == short_url_2

def test_shorten_url_duplicate_does_not_advance_identifier():
    service = {}  # Initialize a new service
    short_url_1 = shorten_url("https://example.com/page", service=service)
    short_url_2 = shorten_url("https://example.com/page", service=service)
    short_url_3 = shorten_url("https://example.com/new-page", service=service)
    # short_url_1 and short_url_2 should be the same, and short_url_3 should get the next identifier
    assert short_url_1 == short_url_2
    assert short_url_3 == "https://short.url/1"  # next identifier after "0"

def test_lookup_url_short_url():
    service = {}  # Initialize a new service
    original_url = "https://example.com/page"
    short_url = shorten_url(original_url, service=service)
    assert lookup_url(short_url, service=service) == original_url

def test_lookup_url_long_url():
    service = {}  # Initialize a new service
    original_url = "https://example.com/page"
    short_url = shorten_url(original_url, service=service)
    assert lookup_url(original_url, service=service) == short_url

def test_lookup_unknown_short_url():
    service = {}  # Initialize a new service
    # Looking up a short URL that is unknown should raise an error
    with pytest.raises(ValueError) as exc:
        lookup_url("https://short.url/unknown", service=service)
    assert str(exc.value) == "Unknown URL: 'https://short.url/unknown'"

def test_lookup_unknown_long_url():
    service = {}  # Initialize a new service
    # Looking up a long URL that is unknown should raise an error
    with pytest.raises(ValueError) as exc:
        lookup_url("https://example.com/unknown", service=service)
    assert str(exc.value) == "Unknown URL: 'https://example.com/unknown'"

def test_get_stats_freshly_shortened_url():
    service = {}  # Initialize a new service
    short_url = shorten_url("https://example.com/page", service=service)
    stats = get_stats(short_url, service=service)
    assert stats['short_url'] == short_url
    assert stats['long_url'] == "https://example.com/page"
    assert stats['visits'] == 0

def test_get_stats_after_visit():
    service = {}  # Initialize a new service
    short_url = shorten_url("https://example.com/page", service=service)
    lookup_url(short_url, service=service)  # This counts as a visit
    stats = get_stats(short_url, service=service)
    assert stats['visits'] == 1

def test_get_stats_long_url():
    service = {}  # Initialize a new service
    short_url = shorten_url("https://example.com/page", service=service)
    lookup_url(short_url, service=service)  # This counts as a visit
    stats_short = get_stats(short_url, service=service)
    stats_long = get_stats("https://example.com/page", service=service)
    assert stats_short == stats_long

def test_get_stats_unknown_url():
    service = {}  # Initialize a new service
    # Requesting stats for an unknown URL should raise an error
    with pytest.raises(ValueError) as exc:
        get_stats("https://example.com/unknown", service=service)
    assert str(exc.value) == "Unknown URL: 'https://example.com/unknown'"

def test_invalid_url_no_scheme():
    # Invalid URL without http or https should raise an error
    with pytest.raises(ValueError) as exc:
        shorten_url("example.com/page")
    assert str(exc.value) == "Invalid URL: 'example.com/page'"

def test_invalid_url_bare_http_scheme():
    # Invalid URL that is only a scheme should raise an error
    with pytest.raises(ValueError) as exc:
        shorten_url("http://")
    assert str(exc.value) == "Invalid URL: 'http://'"

def test_invalid_url_bare_https_scheme():
    # Invalid URL that is only a scheme should raise an error
    with pytest.raises(ValueError) as exc:
        shorten_url("https://")
    assert str(exc.value) == "Invalid URL: 'https://'"

def test_get_stats_no_clock():
    # Without a supplied clock, visits are counted but history stays empty
    service = {}  # Initialize a new service
    short_url = shorten_url("https://example.com/page", service=service)
    lookup_url(short_url, service=service)  # This counts as a visit
    stats = get_stats(short_url, service=service)
    assert stats['visit_history'] == []  # The visit history should be empty

def test_get_stats_with_clock():
    # With a clock, timestamps should be recorded
    from datetime import datetime
    
    def fake_clock():
        return datetime(2026, 1, 1, 12, 0, 0)
    
    service = {}  # Initialize a new service with clock
    short_url = shorten_url("https://example.com/page", service=service, clock=fake_clock)
    lookup_url(short_url, service=service)  # This counts as a visit
    stats = get_stats(short_url, service=service)
    assert stats['visit_history'] == ["2026-01-01 12:00:00"]

def test_get_stats_with_multiple_visits_and_clock():
    # With a clock, multiple timestamps should be recorded in order
    from datetime import datetime
    
    def fake_clock():
        return datetime.now()  # Just return current time
    
    service = {}  # Initialize a new service with clock
    short_url = shorten_url("https://example.com/page", service=service, clock=fake_clock)
    
    # Simulate multiple visits
    lookup_url(short_url, service=service)  # Visit 1
    lookup_url(short_url, service=service)  # Visit 2
    stats = get_stats(short_url, service=service)
    assert len(stats['visit_history']) == 2  # Two visits should be recorded

def test_log_structure():
    # Testing the log structure of a link
    from datetime import datetime
    
    def fake_clock():
        return datetime(2026, 1, 1, 12, 0, 0)
    
    service = {}  # Initialize a new service with clock
    short_url = shorten_url("https://example.com/page", service=service, clock=fake_clock)
    lookup_url(short_url, service=service)  # This counts as a visit
    stats = get_stats(short_url, service=service)
    
    expected_log = (
        f"short_url: {short_url}\n"
        f"long_url: https://example.com/page\n"
        f"visits: {stats['visits']}\n"
        f"{stats['visit_history'][0]}"
    )
    # Here we directly check the log structure
    log_output = (
        f"short_url: {short_url}\n"
        f"long_url: https://example.com/page\n"
        f"visits: 1\n"
        f"2026-01-01 12:00:00"
    )
    assert expected_log == log_output
import pytest
from solution import shorten_url, translate_url, get_url_statistics

@pytest.fixture(autouse=True)
def reset_service():
    # Reset or create a new service instance before each test
    pass  # Implementation of the service reset should be handled here

def test_issue_deterministic_short_urls():
    # AC-1.1
    assert shorten_url("https://example.com/page1") == "https://short.url/0"
    assert shorten_url("https://example.com/page2") == "https://short.url/1"
    # AC-1.2
    assert shorten_url("https://example.com/page3") == "https://short.url/2"  # 3rd distinct URL
    assert shorten_url("https://example.com/page4") == "https://short.url/3"  # 4th distinct URL
    assert shorten_url("https://example.com/page5") == "https://short.url/4"  # 5th distinct URL
    assert shorten_url("https://example.com/page6") == "https://short.url/5"  # 6th distinct URL
    assert shorten_url("https://example.com/page7") == "https://short.url/6"  # 7th distinct URL
    assert shorten_url("https://example.com/page8") == "https://short.url/7"  # 8th distinct URL
    assert shorten_url("https://example.com/page9") == "https://short.url/8"  # 9th distinct URL
    assert shorten_url("https://example.com/page10") == "https://short.url/9"  # 10th distinct URL
    assert shorten_url("https://example.com/page11") == "https://short.url/a"  # 11th distinct URL
    assert shorten_url("https://example.com/page12") == "https://short.url/b"  # 12th distinct URL
    assert shorten_url("https://example.com/page13") == "https://short.url/c"  # 13th distinct URL
    assert shorten_url("https://example.com/page14") == "https://short.url/d"  # 14th distinct URL
    assert shorten_url("https://example.com/page15") == "https://short.url/e"  # 15th distinct URL
    assert shorten_url("https://example.com/page16") == "https://short.url/f"  # 16th distinct URL
    assert shorten_url("https://example.com/page17") == "https://short.url/g"  # 17th distinct URL
    # Thirty-seventh distinct URL
    assert shorten_url("https://example.com/page37") == "https://short.url/10"  # 37th distinct URL

def test_configurable_base_address():
    # AC-1.4
    assert shorten_url("https://example.com/page1", base_address="https://tiny.url/") == "https://tiny.url/0"

def test_identifier_source():
    # AC-1.5
    custom_identifiers = iter(["custom1", "custom2"])
    assert shorten_url("https://example.com/page1", identifier_source=custom_identifiers) == "https://short.url/custom1"
    assert shorten_url("https://example.com/page2", identifier_source=custom_identifiers) == "https://short.url/custom2"

def test_translate_short_to_long():
    # AC-2.1
    short_url = shorten_url("https://example.com/page1")
    assert translate_url(short_url) == "https://example.com/page1"

def test_translate_long_to_short():
    # AC-2.2
    long_url = "https://example.com/page1"
    short_url = shorten_url(long_url)
    assert translate_url(long_url) == short_url

def test_duplicate_shortening():
    # AC-2.3
    short_url = shorten_url("https://example.com/page1")
    assert shorten_url("https://example.com/page1") == short_url  # should return the same short URL

def test_identifier_sequence_not_advanced_on_duplicate():
    # AC-2.4
    shorten_url("https://example.com/page1")
    assert shorten_url("https://example.com/page1") == "https://short.url/0"  # still 0
    assert shorten_url("https://example.com/page2") == "https://short.url/1"  # next distinct should be 1

def test_statistics_initial_visit_count():
    # AC-3.1
    short_url = shorten_url("https://example.com/page1")
    stats = get_url_statistics(short_url)
    assert stats['visits'] == 0

def test_count_visits():
    # AC-3.2
    short_url = shorten_url("https://example.com/page1")
    translate_url(short_url)  # translate counts as visit
    stats = get_url_statistics(short_url)
    assert stats['visits'] == 1

def test_translate_long_does_not_count_visit():
    # AC-3.3
    short_url = shorten_url("https://example.com/page1")
    assert translate_url("https://example.com/page1") == short_url
    stats = get_url_statistics(short_url)
    assert stats['visits'] == 0  # still 0 visits

def test_statistics_record():
    # AC-3.4
    short_url = shorten_url("https://example.com/page1")
    stats = get_url_statistics(short_url)
    assert stats['short_url'] == short_url
    assert stats['long_url'] == "https://example.com/page1"
    assert stats['visits'] == 0

def test_visit_timestamp_logging():
    # AC-3.5
    from datetime import datetime
    short_url = shorten_url("https://example.com/page1")
    translate_url(short_url, clock=datetime(2026, 1, 1, 12, 0, 0))  # visit with timestamp
    stats = get_url_statistics(short_url)
    assert stats['visit_timestamps'] == ["2026-01-01 12:00:00"]

def test_no_clock_empty_history():
    # AC-3.6
    short_url = shorten_url("https://example.com/page1")
    translate_url(short_url)  # visit without clock
    stats = get_url_statistics(short_url)
    assert stats['visit_timestamps'] == []  # history should be empty

def test_statistics_log_format():
    # AC-3.7
    from datetime import datetime
    short_url = shorten_url("https://example.com/page1")
    translate_url(short_url, clock=datetime(2026, 1, 1, 12, 0, 0))  # visit with timestamp
    stats = get_url_statistics(short_url)
    log = f"short_url: {short_url}\nlong_url: https://example.com/page1\nvisits: 1\n2026-01-01 12:00:00"
    assert stats['log'] == log

def test_invalid_url_rejection():
    # AC-4.1
    with pytest.raises(Exception) as exc:
        shorten_url("invalid_url")
    assert str(exc.value) == "Invalid URL: 'invalid_url'"

def test_bare_scheme_rejection():
    # AC-4.2
    with pytest.raises(Exception) as exc:
        shorten_url("http://")
    assert str(exc.value) == "Invalid URL: 'http://'"

    with pytest.raises(Exception) as exc:
        shorten_url("https://")
    assert str(exc.value) == "Invalid URL: 'https://'"

def test_unknown_short_url_translation():
    # AC-4.3
    with pytest.raises(Exception) as exc:
        translate_url("https://short.url/unknown")
    assert str(exc.value) == "Unknown URL: 'https://short.url/unknown'"

def test_unknown_long_url_statistics():
    # AC-4.4
    with pytest.raises(Exception) as exc:
        get_url_statistics("https://example.com/unknown")
    assert str(exc.value) == "Unknown URL: 'https://example.com/unknown'"

def test_non_http_url_rejection():
    # New test for non-HTTP(S) URL rejection
    with pytest.raises(Exception) as exc:
        shorten_url("ftp://example.com")
    assert str(exc.value) == "Invalid URL: 'ftp://example.com'"
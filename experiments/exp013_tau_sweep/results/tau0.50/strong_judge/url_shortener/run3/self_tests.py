import pytest
from solution import URLShortener

def test_issue_deterministic_short_urls():
    service = URLShortener()

    # AC-1.1
    assert service.shorten("https://example.com") == "https://short.url/0"
    # AC-1.1
    assert service.shorten("https://another-example.com") == "https://short.url/1"
    # AC-1.1
    assert service.shorten("https://example.com/page1") == "https://short.url/2"
    assert service.shorten("https://example.com/page2") == "https://short.url/3"
    # AC-1.2
    assert service.shorten("https://example.com/page10") == "https://short.url/4"  # 4 in base 36
    assert service.shorten("https://example.com/page36") == "https://short.url/5"  # 5 in base 36
    assert service.shorten("https://example.com/page37") == "https://short.url/6"  # 6 in base 36
    assert service.shorten("https://example.com/page38") == "https://short.url/a"  # a in base 36
    assert service.shorten("https://example.com/page1000") == "https://short.url/10"  # 10 in base 36

def test_configurable_base_address():
    service = URLShortener(base_address="https://my.short.url/")
    assert service.shorten("https://example.com") == "https://my.short.url/0"

def test_identifier_source():
    service = URLShortener(identifier_source=["foo", "bar", "baz"])
    assert service.shorten("https://example.com") == "https://short.url/foo"  # base address + identifier
    assert service.shorten("https://another-example.com") == "https://short.url/bar"  # base address + identifier
    assert service.shorten("https://example.com") == "https://short.url/foo"  # duplicate = existing
    assert service.shorten("https://new-url.com") == "https://short.url/baz"  # base address + identifier

def test_duplicate_does_not_advance_identifier():
    service = URLShortener()
    service.shorten("https://example.com")
    short_url_1 = service.shorten("https://example.com")
    short_url_2 = service.shorten("https://another-example.com")
    assert short_url_1 == "https://short.url/0"
    assert short_url_2 == "https://short.url/1"

def test_translate_short_to_long():
    service = URLShortener()
    service.shorten("https://example.com")
    assert service.translate("https://short.url/0") == "https://example.com"

def test_translate_long_to_short():
    service = URLShortener()
    service.shorten("https://example.com")
    assert service.translate("https://example.com") == "https://short.url/0"

def test_duplicate_shorten_returns_existing_short_url():
    service = URLShortener()
    short_url = service.shorten("https://example.com")
    assert service.shorten("https://example.com") == short_url

def test_freshly_shortened_url_has_zero_visits():
    service = URLShortener()
    service.shorten("https://example.com")
    stats = service.get_statistics("https://short.url/0")
    assert stats['visits'] == 0

def test_translation_counts_as_one_visit():
    service = URLShortener()
    service.shorten("https://example.com")
    service.translate("https://short.url/0")
    stats = service.get_statistics("https://short.url/0")
    assert stats['visits'] == 1

def test_translating_long_url_does_not_count_as_visit():
    service = URLShortener()
    service.shorten("https://example.com")
    service.translate("https://short.url/0")  # counts as visit
    service.translate("https://example.com")  # does not count as visit
    stats = service.get_statistics("https://short.url/0")
    assert stats['visits'] == 1

def test_statistics_report_short_url():
    service = URLShortener()
    service.shorten("https://example.com")
    service.translate("https://short.url/0")
    stats = service.get_statistics("https://short.url/0")
    assert stats['short_url'] == "https://short.url/0"
    assert stats['long_url'] == "https://example.com"
    assert stats['visits'] == 1

def test_statistics_report_long_url():
    service = URLShortener()
    service.shorten("https://example.com")
    service.translate("https://short.url/0")
    stats = service.get_statistics("https://example.com")
    assert stats['short_url'] == "https://short.url/0"
    assert stats['long_url'] == "https://example.com"
    assert stats['visits'] == 1

def test_visit_timestamps_with_clock():
    from datetime import datetime
    class FakeClock:
        def __init__(self):
            self.current_time = 0
            
        def now(self):
            self.current_time += 1
            return datetime(2026, 1, 1, 12, 0, 0)  # Increment for every call
            
    service = URLShortener(clock=FakeClock())
    service.shorten("https://example.com")
    service.translate("https://short.url/0")
    stats = service.get_statistics("https://short.url/0")
    assert len(stats['timestamps']) == 1
    assert stats['timestamps'][0] == datetime(2026, 1, 1, 12, 0, 0)

def test_visit_timestamps_without_clock():
    service = URLShortener()
    service.shorten("https://example.com")
    service.translate("https://short.url/0")
    stats = service.get_statistics("https://short.url/0")
    assert stats['timestamps'] == []

def test_link_log_format_with_timestamps():
    from datetime import datetime
    class FakeClock:
        def __init__(self):
            self.current_time = 0
            
        def now(self):
            self.current_time += 1
            return datetime(2026, 1, 1, 12, 0, 0)  # Increment for every call
            
    service = URLShortener(clock=FakeClock())
    service.shorten("https://example.com")
    service.translate("https://short.url/0")
    stats = service.get_statistics("https://short.url/0")
    expected_log = (
        "short_url: https://short.url/0\n"
        "long_url: https://example.com\n"
        "visits: 1\n"
        "2026-01-01 12:00:00\n"
    )
    assert service.get_log("https://short.url/0") == expected_log

def test_link_log_format_without_timestamps():
    service = URLShortener()
    service.shorten("https://example.com")
    service.translate("https://short.url/0")
    stats = service.get_statistics("https://short.url/0")
    expected_log = (
        "short_url: https://short.url/0\n"
        "long_url: https://example.com\n"
        "visits: 1\n"
    )
    assert service.get_log("https://short.url/0") == expected_log

def test_invalid_url_without_scheme():
    service = URLShortener()
    with pytest.raises(Exception) as exc:
        service.shorten("not_a_url")
    assert str(exc.value) == "Invalid URL: 'not_a_url'"

def test_invalid_url_bare_scheme():
    service = URLShortener()
    with pytest.raises(Exception) as exc:
        service.shorten("https://")
    assert str(exc.value) == "Invalid URL: 'https://'"

def test_invalid_url_non_web_scheme():
    service = URLShortener()
    with pytest.raises(Exception) as exc:
        service.shorten("ftp://example.com")
    assert str(exc.value) == "Invalid URL: 'ftp://example.com'"

def test_unknown_short_url_translation():
    service = URLShortener()
    with pytest.raises(Exception) as exc:
        service.translate("https://short.url/unknown")
    assert str(exc.value) == "Unknown URL: 'https://short.url/unknown'"

def test_unknown_long_url_statistics():
    service = URLShortener()
    with pytest.raises(Exception) as exc:
        service.get_statistics("https://example.com")
    assert str(exc.value) == "Unknown URL: 'https://example.com'"

def test_unknown_short_url_statistics():
    service = URLShortener()
    with pytest.raises(Exception) as exc:
        service.get_statistics("https://short.url/unknown")
    assert str(exc.value) == "Unknown URL: 'https://short.url/unknown'"
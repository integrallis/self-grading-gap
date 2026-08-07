import pytest
import re
from solution import decompose_url

def test_decompose_url_with_canonical_example():
    url = "http://foo.bar.com/foobar.html"
    expected = {
        "protocol": "http",  # protocol is "http"
        "subdomain": "foo",  # subdomain is "foo"
        "domain": "bar.com", # domain is "bar.com"
        "port": 80,          # default port for http is 80
        "path": "foobar.html", # path is "foobar.html"
        "query": "",         # no query string present
        "anchor": ""         # no anchor present
    }
    assert decompose_url(url) == expected

def test_decompose_url_with_explicit_port_and_full_path():
    url = "https://www.foobar.com:8080/download/install.exe"
    expected = {
        "protocol": "https",  # protocol is "https"
        "subdomain": "www",    # subdomain is "www"
        "domain": "foobar.com", # domain is "foobar.com"
        "port": 8080,          # explicit port is 8080
        "path": "download/install.exe", # path is "download/install.exe"
        "query": "",           # no query string present
        "anchor": ""           # no anchor present
    }
    assert decompose_url(url) == expected

def test_decompose_url_with_dotted_host():
    url = "http://a.b.bar.com/path/to/resource"
    expected = {
        "protocol": "http",    # protocol is "http"
        "subdomain": "a.b",    # subdomain is "a.b"
        "domain": "bar.com",   # domain is "bar.com"
        "port": 80,            # default port for http is 80
        "path": "path/to/resource", # path is "path/to/resource"
        "query": "",           # no query string present
        "anchor": ""           # no anchor present
    }
    assert decompose_url(url) == expected

def test_decompose_url_with_localhost():
    url = "http://localhost:3000/path"
    expected = {
        "protocol": "http",    # protocol is "http"
        "subdomain": "",       # empty subdomain for localhost
        "domain": "localhost", # domain is "localhost"
        "port": 3000,          # explicit port is 3000
        "path": "path",        # path is "path"
        "query": "",           # no query string present
        "anchor": ""           # no anchor present
    }
    assert decompose_url(url) == expected

def test_decompose_url_with_no_path():
    url = "http://example.com"
    expected = {
        "protocol": "http",    # protocol is "http"
        "subdomain": "",       # empty subdomain
        "domain": "example.com", # domain is "example.com"
        "port": 80,            # default port for http is 80
        "path": "",            # no path present
        "query": "",           # no query string present
        "anchor": ""           # no anchor present
    }
    assert decompose_url(url) == expected

def test_decompose_url_with_bare_trailing_slash():
    url = "http://example.com/"
    expected = {
        "protocol": "http",    # protocol is "http"
        "subdomain": "",       # empty subdomain
        "domain": "example.com", # domain is "example.com"
        "port": 80,            # default port for http is 80
        "path": "",            # path is empty
        "query": "",           # no query string present
        "anchor": ""           # no anchor present
    }
    assert decompose_url(url) == expected

def test_decompose_url_with_query_string():
    url = "http://example.com?query=123"
    expected = {
        "protocol": "http",    # protocol is "http"
        "subdomain": "",       # empty subdomain
        "domain": "example.com", # domain is "example.com"
        "port": 80,            # default port for http is 80
        "path": "",            # no path present
        "query": "query=123",  # query string is "query=123"
        "anchor": ""           # no anchor present
    }
    assert decompose_url(url) == expected

def test_decompose_url_with_anchor():
    url = "http://example.com#section1"
    expected = {
        "protocol": "http",    # protocol is "http"
        "subdomain": "",       # empty subdomain
        "domain": "example.com", # domain is "example.com"
        "port": 80,            # default port for http is 80
        "path": "",            # no path present
        "query": "",           # no query string present
        "anchor": "section1"   # anchor is "section1"
    }
    assert decompose_url(url) == expected

def test_decompose_url_with_query_and_anchor():
    url = "http://www.example.com/path?q=1#top"
    expected = {
        "protocol": "http",    # protocol is "http"
        "subdomain": "www",    # subdomain is "www"
        "domain": "example.com", # domain is "example.com"
        "port": 80,            # default port for http is 80
        "path": "path",        # path is "path"
        "query": "q=1",        # query string is "q=1"
        "anchor": "top"        # anchor is "top"
    }
    assert decompose_url(url) == expected

def test_decompose_url_with_no_protocol():
    url = "example.com"
    expected_message = "Malformed URL, missing '://': 'example.com'"
    with pytest.raises(Exception, match=rf"^{re.escape(expected_message)}$"):
        decompose_url(url)

def test_decompose_url_with_unsupported_protocol():
    url = "gopher://example.com"
    expected_message = "Unsupported protocol: 'gopher'"
    with pytest.raises(Exception, match=rf"^{re.escape(expected_message)}$"):
        decompose_url(url)

def test_decompose_url_with_ftp_protocol():
    url = "ftp://example.com"
    expected = {
        "protocol": "ftp",     # protocol is "ftp"
        "subdomain": "",       # empty subdomain
        "domain": "example.com", # domain is "example.com"
        "port": 21,            # default port for ftp is 21
        "path": "",            # no path present
        "query": "",           # no query string present
        "anchor": ""           # no anchor present
    }
    assert decompose_url(url) == expected

def test_decompose_url_with_sftp_protocol():
    url = "sftp://example.com"
    expected = {
        "protocol": "sftp",    # protocol is "sftp"
        "subdomain": "",       # empty subdomain
        "domain": "example.com", # domain is "example.com"
        "port": 22,            # default port for sftp is 22
        "path": "",            # no path present
        "query": "",           # no query string present
        "anchor": ""           # no anchor present
    }
    assert decompose_url(url) == expected

def test_decompose_url_with_missing_host():
    url = "http://"
    expected_message = "Missing host"
    with pytest.raises(Exception, match=rf"^{re.escape(expected_message)}$"):
        decompose_url(url)

def test_decompose_url_with_unsupported_tld():
    url = "http://example.xyz"
    expected_message = "Unsupported top-level domain: 'xyz'"
    with pytest.raises(Exception, match=rf"^{re.escape(expected_message)}$"):
        decompose_url(url)

def test_decompose_url_with_multi_label_unsupported_tld():
    url = "http://a.b.example.xyz"
    expected_message = "Unsupported top-level domain: 'xyz'"
    with pytest.raises(Exception, match=rf"^{re.escape(expected_message)}$"):
        decompose_url(url)

def test_decompose_url_with_invalid_port():
    url = "http://example.com:abc"
    expected_message = "Invalid port: 'abc'"
    with pytest.raises(Exception, match=rf"^{re.escape(expected_message)}$"):
        decompose_url(url)

def test_decompose_url_with_multiple_colons_in_port():
    url = "http://example.com:8080:9090"
    expected_message = "Invalid port: '8080:9090'"
    with pytest.raises(Exception, match=rf"^{re.escape(expected_message)}$"):
        decompose_url(url)

def test_decompose_url_with_embedded_url_in_query():
    url = "http://example.com?next=https://other.com/path"
    expected = {
        "protocol": "http",    # protocol is "http"
        "subdomain": "",       # empty subdomain
        "domain": "example.com", # domain is "example.com"
        "port": 80,            # default port for http is 80
        "path": "",            # no path present
        "query": "next=https://other.com/path", # query string is "next=https://other.com/path"
        "anchor": ""           # no anchor present
    }
    assert decompose_url(url) == expected

def test_decompose_url_with_supported_tlds():
    supported_tlds = ['net', 'org', 'int', 'edu', 'gov', 'mil']
    for tld in supported_tlds:
        url = f"http://example.{tld}"
        expected = {
            "protocol": "http",    # protocol is "http"
            "subdomain": "",       # empty subdomain
            "domain": f"example.{tld}", # domain is "example.{tld}"
            "port": 80,            # default port for http is 80
            "path": "",            # no path present
            "query": "",           # no query string present
            "anchor": ""           # no anchor present
        }
        assert decompose_url(url) == expected
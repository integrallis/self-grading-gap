# your complete test file
import pytest
from solution import decompose_url

def test_decompose_url_http_with_path():
    result = decompose_url("http://foo.bar.com/foobar.html")
    # expected: protocol = "http", subdomain = "foo", domain = "bar.com", port = 80, path = "foobar.html"
    assert result["protocol"] == "http"
    assert result["subdomain"] == "foo"
    assert result["domain"] == "bar.com"
    assert result["port"] == 80
    assert result["path"] == "foobar.html"
    assert result["query"] == ""
    assert result["anchor"] == ""

def test_decompose_url_https_with_explicit_port():
    result = decompose_url("https://www.foobar.com:8080/download/install.exe")
    # expected: protocol = "https", subdomain = "www", domain = "foobar.com", port = 8080, path = "download/install.exe"
    assert result["protocol"] == "https"
    assert result["subdomain"] == "www"
    assert result["domain"] == "foobar.com"
    assert result["port"] == 8080
    assert result["path"] == "download/install.exe"
    assert result["query"] == ""
    assert result["anchor"] == ""

def test_decompose_url_subdomain_with_multiple_labels():
    result = decompose_url("http://a.b.bar.com/path")
    # expected: subdomain = "a.b", domain = "bar.com"
    assert result["subdomain"] == "a.b"
    assert result["domain"] == "bar.com"

def test_decompose_url_empty_subdomain():
    result = decompose_url("http://bar.com/path")
    # expected: subdomain = "", domain = "bar.com"
    assert result["subdomain"] == ""
    assert result["domain"] == "bar.com"

def test_decompose_url_localhost():
    result = decompose_url("http://localhost:8080/path")
    # expected: subdomain = "", domain = "localhost", port = 8080, path = "path"
    assert result["subdomain"] == ""
    assert result["domain"] == "localhost"
    assert result["port"] == 8080
    assert result["path"] == "path"

def test_decompose_url_no_path():
    result = decompose_url("http://foo.bar.com")
    # expected: path = ""
    assert result["path"] == ""

def test_decompose_url_trailing_slash():
    result = decompose_url("http://foo.bar.com/")
    # expected: path = ""
    assert result["path"] == ""

def test_decompose_url_with_query_string():
    result = decompose_url("http://foo.bar.com/path?query=1")
    # expected: query = "query=1", path = "path"
    assert result["query"] == "query=1"
    assert result["path"] == "path"

def test_decompose_url_with_anchor():
    result = decompose_url("http://foo.bar.com/path#section1")
    # expected: anchor = "section1", path = "path"
    assert result["anchor"] == "section1"
    assert result["path"] == "path"

def test_decompose_url_with_query_and_anchor():
    result = decompose_url("http://foo.bar.com/path?query=1#section1")
    # expected: query = "query=1", anchor = "section1", path = "path"
    assert result["query"] == "query=1"
    assert result["anchor"] == "section1"
    assert result["path"] == "path"

def test_decompose_url_query_string_without_path():
    result = decompose_url("http://foo.bar.com?query=1")
    # expected: path = ""
    assert result["path"] == ""
    assert result["query"] == "query=1"

def test_decompose_url_invalid_protocol():
    result = decompose_url("gopher://foo.bar.com")
    # expected: "Unsupported protocol: 'gopher'"
    assert result == "Unsupported protocol: 'gopher'"

def test_decompose_url_missing_colon():
    result = decompose_url("foo.bar.com")
    # expected: "Malformed URL, missing '://': 'foo.bar.com'"
    assert result == "Malformed URL, missing '://': 'foo.bar.com'"

def test_decompose_url_unsupported_tld():
    result = decompose_url("http://foo.bar.xyz")
    # expected: "Unsupported top-level domain: 'xyz'"
    assert result == "Unsupported top-level domain: 'xyz'"

def test_decompose_url_invalid_port():
    result = decompose_url("http://foo.bar.com:abc")
    # expected: "Invalid port: 'abc'"
    assert result == "Invalid port: 'abc'"

def test_decompose_url_missing_host():
    result = decompose_url("http:///path")
    # expected: "Missing host"
    assert result == "Missing host"

def test_decompose_url_multiple_colons_in_port():
    result = decompose_url("http://foo.com:8080:9090/path")
    # expected: "Invalid port: '8080:9090'"
    assert result == "Invalid port: '8080:9090'"

def test_decompose_url_with_ftp_default_port():
    result = decompose_url("ftp://example.com")
    # expected: protocol = "ftp", port = 21
    assert result["protocol"] == "ftp"
    assert result["port"] == 21

def test_decompose_url_with_https_default_port():
    result = decompose_url("https://example.com")
    # expected: protocol = "https", port = 443
    assert result["protocol"] == "https"
    assert result["port"] == 443

def test_decompose_url_with_sftp_default_port():
    result = decompose_url("sftp://example.com")
    # expected: protocol = "sftp", port = 22
    assert result["protocol"] == "sftp"
    assert result["port"] == 22

def test_decompose_url_with_recognized_tlds():
    tlds = ["com", "net", "org", "int", "edu", "gov", "mil"]
    for tld in tlds:
        result = decompose_url(f"http://foo.bar.{tld}")
        assert result["domain"] == f"bar.{tld}"
        assert result["subdomain"] == "foo"

def test_decompose_url_direct_host_query():
    result = decompose_url("http://foo.bar.com?query=1")
    # expected: path = "", query = "query=1"
    assert result["path"] == ""
    assert result["query"] == "query=1"

def test_decompose_url_embedded_url_in_query():
    result = decompose_url("http://foo.bar.com/path?next=https://example.com/a")
    # expected: embedded URL remains verbatim in query
    assert result["query"] == "next=https://example.com/a"
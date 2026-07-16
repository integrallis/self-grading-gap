import pytest
from solution import decompose_url

def test_decompose_url_http_example():
    result = decompose_url("http://foo.bar.com/foobar.html")
    # Expected: protocol "http", subdomain "foo", domain "bar.com", port 80, path "foobar.html"
    assert result["protocol"] == "http"
    assert result["subdomain"] == "foo"
    assert result["domain"] == "bar.com"
    assert result["port"] == 80
    assert result["path"] == "foobar.html"
    assert result["query"] == ""
    assert result["anchor"] == ""

def test_decompose_url_https_example():
    result = decompose_url("https://www.foobar.com:8080/download/install.exe")
    # Expected: protocol "https", subdomain "www", domain "foobar.com", port 8080, path "download/install.exe"
    assert result["protocol"] == "https"
    assert result["subdomain"] == "www"
    assert result["domain"] == "foobar.com"
    assert result["port"] == 8080
    assert result["path"] == "download/install.exe"
    assert result["query"] == ""
    assert result["anchor"] == ""

def test_decompose_url_subdomain():
    result = decompose_url("http://a.b.bar.com/path")
    # Expected: subdomain "a.b", domain "bar.com"
    assert result["subdomain"] == "a.b"
    assert result["domain"] == "bar.com"

def test_decompose_url_empty_subdomain():
    result = decompose_url("http://bar.com/path")
    # Expected: empty subdomain
    assert result["subdomain"] == ""

def test_decompose_url_localhost():
    result = decompose_url("http://localhost:3000/path")
    # Expected: domain "localhost", empty subdomain, port 3000, path "path"
    assert result["domain"] == "localhost"
    assert result["subdomain"] == ""
    assert result["port"] == 3000
    assert result["path"] == "path"

def test_decompose_url_empty_path():
    result = decompose_url("http://example.com/")
    # Expected: empty path
    assert result["path"] == ""

def test_decompose_url_no_path():
    result = decompose_url("http://example.com")
    # Expected: empty path
    assert result["path"] == ""

def test_decompose_url_default_port_http():
    result = decompose_url("http://example.com/path")
    # Expected: port 80 (default for http)
    assert result["port"] == 80

def test_decompose_url_default_port_https():
    result = decompose_url("https://example.com/path")
    # Expected: port 443 (default for https)
    assert result["port"] == 443

def test_decompose_url_default_port_ftp():
    result = decompose_url("ftp://example.com/path")
    # Expected: port 21 (default for ftp)
    assert result["port"] == 21

def test_decompose_url_default_port_sftp():
    result = decompose_url("sftp://example.com/path")
    # Expected: port 22 (default for sftp)
    assert result["port"] == 22

def test_decompose_url_explicit_port():
    result = decompose_url("ftp://example.com:21/path")
    # Expected: port 21 (explicit)
    assert result["port"] == 21

def test_decompose_url_unsupported_protocol():
    with pytest.raises(Exception) as excinfo:
        decompose_url("gopher://example.com")
    assert str(excinfo.value) == "Unsupported protocol: 'gopher'"

def test_decompose_url_missing_protocol():
    with pytest.raises(Exception) as excinfo:
        decompose_url("example.com/path")
    assert str(excinfo.value) == "Malformed URL, missing '://': 'example.com/path'"

def test_decompose_url_unsupported_tld():
    with pytest.raises(Exception) as excinfo:
        decompose_url("http://example.xyz/path")
    assert str(excinfo.value) == "Unsupported top-level domain: 'xyz'"

def test_decompose_url_invalid_port():
    with pytest.raises(Exception) as excinfo:
        decompose_url("http://example.com:abc/path")
    assert str(excinfo.value) == "Invalid port: 'abc'"

def test_decompose_url_missing_host():
    with pytest.raises(Exception) as excinfo:
        decompose_url("http:///path")
    assert str(excinfo.value) == "Missing host"

def test_decompose_url_query_string():
    result = decompose_url("http://example.com/path?query=1")
    # Expected: query string "query=1"
    assert result["query"] == "query=1"
    assert result["path"] == "path"

def test_decompose_url_anchor():
    result = decompose_url("http://example.com/path#section")
    # Expected: anchor "section"
    assert result["anchor"] == "section"
    assert result["path"] == "path"

def test_decompose_url_query_and_anchor():
    result = decompose_url("http://www.example.com/path?query=1#section")
    # Expected: query string "query=1", anchor "section", subdomain "www", domain "example.com", path "path"
    assert result["query"] == "query=1"
    assert result["anchor"] == "section"
    assert result["subdomain"] == "www"
    assert result["domain"] == "example.com"
    assert result["path"] == "path"

def test_decompose_url_query_no_path():
    result = decompose_url("http://example.com?query=1")
    # Expected: empty path
    assert result["path"] == ""
    assert result["query"] == "query=1"

def test_decompose_url_embedded_url_in_query():
    result = decompose_url("http://example.com/path?next=http://foo.bar.com/x")
    # Expected: query remains verbatim
    assert result["query"] == "next=http://foo.bar.com/x"

def test_decompose_url_invalid_tld_multi_label():
    with pytest.raises(Exception) as excinfo:
        decompose_url("http://a.b.example.xyz/path")
    assert str(excinfo.value) == "Unsupported top-level domain: 'xyz'"

def test_decompose_url_invalid_port_multi_colon():
    with pytest.raises(Exception) as excinfo:
        decompose_url("http://foo.com:8080:9090/path")
    assert str(excinfo.value) == "Invalid port: '8080:9090'"

def test_decompose_url_recognized_tld_net():
    result = decompose_url("http://example.net")
    # Expected: domain "example.net"
    assert result["domain"] == "example.net"

def test_decompose_url_recognized_tld_org():
    result = decompose_url("http://example.org")
    # Expected: domain "example.org"
    assert result["domain"] == "example.org"

def test_decompose_url_recognized_tld_int():
    result = decompose_url("http://example.int")
    # Expected: domain "example.int"
    assert result["domain"] == "example.int"

def test_decompose_url_recognized_tld_edu():
    result = decompose_url("http://example.edu")
    # Expected: domain "example.edu"
    assert result["domain"] == "example.edu"

def test_decompose_url_recognized_tld_gov():
    result = decompose_url("http://example.gov")
    # Expected: domain "example.gov"
    assert result["domain"] == "example.gov"

def test_decompose_url_recognized_tld_mil():
    result = decompose_url("http://example.mil")
    # Expected: domain "example.mil"
    assert result["domain"] == "example.mil"
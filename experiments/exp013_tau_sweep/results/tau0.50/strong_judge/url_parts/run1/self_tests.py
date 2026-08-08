import pytest
from solution import decompose_url

def test_split_url_with_full_components():
    # Given: "http://foo.bar.com/foobar.html"
    # Expected protocol: "http"
    # Expected subdomain: "foo"
    # Expected domain: "bar.com"
    # Expected port: 80 (default for http)
    # Expected path: "foobar.html"
    assert decompose_url("http://foo.bar.com/foobar.html") == {
        "protocol": "http",
        "subdomain": "foo",
        "domain": "bar.com",
        "port": 80,
        "path": "foobar.html",
        "query": "",
        "anchor": ""
    }

def test_split_url_with_custom_port_and_path():
    # Given: "https://www.foobar.com:8080/download/install.exe"
    # Expected protocol: "https"
    # Expected subdomain: "www"
    # Expected domain: "foobar.com"
    # Expected port: 8080 (explicitly provided)
    # Expected path: "download/install.exe"
    assert decompose_url("https://www.foobar.com:8080/download/install.exe") == {
        "protocol": "https",
        "subdomain": "www",
        "domain": "foobar.com",
        "port": 8080,
        "path": "download/install.exe",
        "query": "",
        "anchor": ""
    }

def test_split_url_with_no_path():
    # Given: "http://example.com/"
    # Expected protocol: "http"
    # Expected subdomain: ""
    # Expected domain: "example.com"
    # Expected port: 80 (default for http)
    # Expected path: "" (no path)
    assert decompose_url("http://example.com/") == {
        "protocol": "http",
        "subdomain": "",
        "domain": "example.com",
        "port": 80,
        "path": "",
        "query": "",
        "anchor": ""
    }

def test_split_url_with_localhost():
    # Given: "http://localhost:3000/path/to/resource"
    # Expected protocol: "http"
    # Expected subdomain: ""
    # Expected domain: "localhost"
    # Expected port: 3000 (explicitly provided)
    # Expected path: "path/to/resource"
    assert decompose_url("http://localhost:3000/path/to/resource") == {
        "protocol": "http",
        "subdomain": "",
        "domain": "localhost",
        "port": 3000,
        "path": "path/to/resource",
        "query": "",
        "anchor": ""
    }

def test_split_url_with_query_string():
    # Given: "http://foo.com?param=value"
    # Expected protocol: "http"
    # Expected subdomain: ""
    # Expected domain: "foo.com"
    # Expected port: 80 (default for http)
    # Expected path: "" (no path)
    # Expected query: "param=value"
    assert decompose_url("http://foo.com?param=value") == {
        "protocol": "http",
        "subdomain": "",
        "domain": "foo.com",
        "port": 80,
        "path": "",
        "query": "param=value",
        "anchor": ""
    }

def test_split_url_with_anchor():
    # Given: "http://example.com#section"
    # Expected protocol: "http"
    # Expected subdomain: ""
    # Expected domain: "example.com"
    # Expected port: 80 (default for http)
    # Expected path: "" (no path)
    # Expected anchor: "section"
    assert decompose_url("http://example.com#section") == {
        "protocol": "http",
        "subdomain": "",
        "domain": "example.com",
        "port": 80,
        "path": "",
        "query": "",
        "anchor": "section"
    }

def test_split_url_with_query_and_anchor():
    # Given: "https://www.example.com/path?q=1#part"
    # Expected protocol: "https"
    # Expected subdomain: "www"
    # Expected domain: "example.com"
    # Expected port: 443 (default for https)
    # Expected path: "path"
    # Expected query: "q=1"
    # Expected anchor: "part"
    assert decompose_url("https://www.example.com/path?q=1#part") == {
        "protocol": "https",
        "subdomain": "www",
        "domain": "example.com",
        "port": 443,
        "path": "path",
        "query": "q=1",
        "anchor": "part"
    }

def test_split_url_with_embedded_url_in_query():
    # Given: "http://example.com?next=https://other.com/x"
    # Expected protocol: "http"
    # Expected subdomain: ""
    # Expected domain: "example.com"
    # Expected port: 80 (default for http)
    # Expected path: "" (no path)
    # Expected query: "next=https://other.com/x"
    assert decompose_url("http://example.com?next=https://other.com/x") == {
        "protocol": "http",
        "subdomain": "",
        "domain": "example.com",
        "port": 80,
        "path": "",
        "query": "next=https://other.com/x",
        "anchor": ""
    }

def test_split_url_with_multi_label_subdomain():
    # Given: "http://a.b.bar.com"
    # Expected protocol: "http"
    # Expected subdomain: "a.b"
    # Expected domain: "bar.com"
    # Expected port: 80 (default for http)
    # Expected path: "" (no path)
    assert decompose_url("http://a.b.bar.com") == {
        "protocol": "http",
        "subdomain": "a.b",
        "domain": "bar.com",
        "port": 80,
        "path": "",
        "query": "",
        "anchor": ""
    }

def test_reject_unsupported_protocol():
    # Given: "gopher://example.com"
    # Expected: "Unsupported protocol: 'gopher'"
    assert decompose_url("gopher://example.com") == "Unsupported protocol: 'gopher'"

def test_reject_missing_colon():
    # Given: "http//example.com"
    # Expected: "Malformed URL, missing '://': 'http//example.com'"
    assert decompose_url("http//example.com") == "Malformed URL, missing '://': 'http//example.com'"

def test_reject_unsupported_tld():
    # Given: "http://example.xyz"
    # Expected: "Unsupported top-level domain: 'xyz'"
    assert decompose_url("http://example.xyz") == "Unsupported top-level domain: 'xyz'"

def test_reject_invalid_port():
    # Given: "http://example.com:abc"
    # Expected: "Invalid port: 'abc'"
    assert decompose_url("http://example.com:abc") == "Invalid port: 'abc'"

def test_reject_missing_host():
    # Given: "http:///path"
    # Expected: "Missing host"
    assert decompose_url("http:///path") == "Missing host"

def test_reject_invalid_port_with_colon():
    # Given: "http://foo.com:8080:9090"
    # Expected: "Invalid port: '8080:9090'"
    assert decompose_url("http://foo.com:8080:9090") == "Invalid port: '8080:9090'"

def test_reject_no_path_with_trailing_slash():
    # Given: "http://example.com/"
    # Expected: path should be empty
    assert decompose_url("http://example.com/") == {
        "protocol": "http",
        "subdomain": "",
        "domain": "example.com",
        "port": 80,
        "path": "",
        "query": "",
        "anchor": ""
    }

def test_default_ports_for_ftp():
    # Given: "ftp://example.com"
    # Expected protocol: "ftp"
    # Expected subdomain: ""
    # Expected domain: "example.com"
    # Expected port: 21 (default for ftp)
    # Expected path: ""
    assert decompose_url("ftp://example.com") == {
        "protocol": "ftp",
        "subdomain": "",
        "domain": "example.com",
        "port": 21,
        "path": "",
        "query": "",
        "anchor": ""
    }

def test_default_ports_for_sftp():
    # Given: "sftp://example.com"
    # Expected protocol: "sftp"
    # Expected subdomain: ""
    # Expected domain: "example.com"
    # Expected port: 22 (default for sftp)
    # Expected path: ""
    assert decompose_url("sftp://example.com") == {
        "protocol": "sftp",
        "subdomain": "",
        "domain": "example.com",
        "port": 22,
        "path": "",
        "query": "",
        "anchor": ""
    }

# Additional tests for coverage of recognised TLDs
@pytest.mark.parametrize("url", [
    "http://example.net",
    "http://example.org",
    "http://example.int",
    "http://example.edu",
    "http://example.gov",
    "http://example.mil"
])
def test_recognised_tlds(url):
    # Expected protocol: "http"
    # Expected subdomain: ""
    # Expected domain: "<TLD>.com"
    # Expected port: 80 (default for http)
    # Expected path: ""
    assert decompose_url(url) == {
        "protocol": "http",
        "subdomain": "",
        "domain": url.split("//")[-1],
        "port": 80,
        "path": "",
        "query": "",
        "anchor": ""
    }

def test_reject_unsupported_tld_multi_label():
    # Given: "http://a.b.example.xyz"
    # Expected: "Unsupported top-level domain: 'xyz'"
    assert decompose_url("http://a.b.example.xyz") == "Unsupported top-level domain: 'xyz'"
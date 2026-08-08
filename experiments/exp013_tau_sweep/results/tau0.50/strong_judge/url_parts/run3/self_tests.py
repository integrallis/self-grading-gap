import pytest
from solution import decompose_url  # Replace with the actual function name defined in the specification

def test_decompose_url_http_canonical():
    result = decompose_url("http://foo.bar.com/foobar.html")
    # protocol: "http", subdomain: "foo", domain: "bar.com", port: 80, path: "foobar.html"
    assert result == {
        'protocol': "http",
        'subdomain': "foo",
        'domain': "bar.com",
        'port': 80,
        'path': "foobar.html",
        'query_string': "",
        'anchor': ""
    }

def test_decompose_url_https_with_explicit_port():
    result = decompose_url("https://www.foobar.com:8080/download/install.exe")
    # protocol: "https", subdomain: "www", domain: "foobar.com", port: 8080, path: "download/install.exe"
    assert result == {
        'protocol': "https",
        'subdomain': "www",
        'domain': "foobar.com",
        'port': 8080,
        'path': "download/install.exe",
        'query_string': "",
        'anchor': ""
    }

def test_decompose_url_multiple_subdomains():
    result = decompose_url("http://a.b.bar.com/test")
    # protocol: "http", subdomain: "a.b", domain: "bar.com", port: 80, path: "test"
    assert result == {
        'protocol': "http",
        'subdomain': "a.b",
        'domain': "bar.com",
        'port': 80,
        'path': "test",
        'query_string': "",
        'anchor': ""
    }

def test_decompose_url_empty_subdomain():
    result = decompose_url("http://bar.com/")
    # protocol: "http", subdomain: "", domain: "bar.com", port: 80, path: ""
    assert result == {
        'protocol': "http",
        'subdomain': "",
        'domain': "bar.com",
        'port': 80,
        'path': "",
        'query_string': "",
        'anchor': ""
    }

def test_decompose_url_localhost():
    result = decompose_url("http://localhost:8080/path")
    # protocol: "http", subdomain: "", domain: "localhost", port: 8080, path: "path"
    assert result == {
        'protocol': "http",
        'subdomain': "",
        'domain': "localhost",
        'port': 8080,
        'path': "path",
        'query_string': "",
        'anchor': ""
    }

def test_decompose_url_no_path():
    result = decompose_url("http://example.com")
    # protocol: "http", subdomain: "", domain: "example.com", port: 80, path: ""
    assert result == {
        'protocol': "http",
        'subdomain': "",
        'domain': "example.com",
        'port': 80,
        'path': "",
        'query_string': "",
        'anchor': ""
    }

def test_decompose_url_with_query_string():
    result = decompose_url("http://example.com?query=1")
    # protocol: "http", subdomain: "", domain: "example.com", port: 80, path: "", query_string: "query=1"
    assert result == {
        'protocol': "http",
        'subdomain': "",
        'domain': "example.com",
        'port': 80,
        'path': "",
        'query_string': "query=1",
        'anchor': ""
    }

def test_decompose_url_with_anchor():
    result = decompose_url("http://example.com#section")
    # protocol: "http", subdomain: "", domain: "example.com", port: 80, path: "", anchor: "section"
    assert result == {
        'protocol': "http",
        'subdomain': "",
        'domain': "example.com",
        'port': 80,
        'path': "",
        'query_string': "",
        'anchor': "section"
    }

def test_decompose_url_with_query_and_anchor():
    result = decompose_url("http://example.com/path?query=1#section")
    # protocol: "http", subdomain: "", domain: "example.com", port: 80, path: "path", query_string: "query=1", anchor: "section"
    assert result == {
        'protocol': "http",
        'subdomain': "",
        'domain': "example.com",
        'port': 80,
        'path': "path",
        'query_string': "query=1",
        'anchor': "section"
    }

def test_decompose_url_empty_query_and_anchor():
    result = decompose_url("http://example.com/path?#")
    # protocol: "http", subdomain: "", domain: "example.com", port: 80, path: "path", query_string: "", anchor: ""
    assert result == {
        'protocol': "http",
        'subdomain': "",
        'domain': "example.com",
        'port': 80,
        'path': "path",
        'query_string': "",
        'anchor': ""
    }

def test_decompose_url_invalid_protocol():
    result = decompose_url("gopher://example.com")
    # Expecting rejection message for unsupported protocol
    assert result == "Unsupported protocol: 'gopher'"

def test_decompose_url_missing_marker():
    result = decompose_url("example.com")
    # Expecting rejection message for missing '://'
    assert result == "Malformed URL, missing '://': 'example.com'"

def test_decompose_url_unsupported_tld():
    result = decompose_url("http://foo.bar.xyz")
    # Expecting rejection message for unsupported TLD
    assert result == "Unsupported top-level domain: 'xyz'"

def test_decompose_url_invalid_port():
    result = decompose_url("http://example.com:foo")
    # Expecting rejection message for invalid port
    assert result == "Invalid port: 'foo'"

def test_decompose_url_missing_host():
    result = decompose_url("http:///path")
    # Expecting rejection message for missing host
    assert result == "Missing host"

# New tests for additional coverage
def test_decompose_url_combined_query_and_anchor_with_subdomain():
    result = decompose_url("http://a.b.example.com/path?q=1#top")
    # protocol: "http", subdomain: "a.b", domain: "example.com", port: 80, path: "path", query_string: "q=1", anchor: "top"
    assert result == {
        'protocol': "http",
        'subdomain': "a.b",
        'domain': "example.com",
        'port': 80,
        'path': "path",
        'query_string': "q=1",
        'anchor': "top"
    }

def test_decompose_url_valid_tld_net():
    result = decompose_url("http://example.net")
    assert result == {
        'protocol': "http",
        'subdomain': "",
        'domain': "example.net",
        'port': 80,
        'path': "",
        'query_string': "",
        'anchor': ""
    }

def test_decompose_url_valid_tld_org():
    result = decompose_url("http://example.org")
    assert result == {
        'protocol': "http",
        'subdomain': "",
        'domain': "example.org",
        'port': 80,
        'path': "",
        'query_string': "",
        'anchor': ""
    }

def test_decompose_url_valid_tld_edu():
    result = decompose_url("http://example.edu")
    assert result == {
        'protocol': "http",
        'subdomain': "",
        'domain': "example.edu",
        'port': 80,
        'path': "",
        'query_string': "",
        'anchor': ""
    }

def test_decompose_url_valid_tld_int():
    result = decompose_url("http://example.int")
    assert result == {
        'protocol': "http",
        'subdomain': "",
        'domain': "example.int",
        'port': 80,
        'path': "",
        'query_string': "",
        'anchor': ""
    }

def test_decompose_url_valid_tld_gov():
    result = decompose_url("http://example.gov")
    assert result == {
        'protocol': "http",
        'subdomain': "",
        'domain': "example.gov",
        'port': 80,
        'path': "",
        'query_string': "",
        'anchor': ""
    }

def test_decompose_url_valid_tld_mil():
    result = decompose_url("http://example.mil")
    assert result == {
        'protocol': "http",
        'subdomain': "",
        'domain': "example.mil",
        'port': 80,
        'path': "",
        'query_string': "",
        'anchor': ""
    }

def test_decompose_url_https_default_port():
    result = decompose_url("https://example.com")
    assert result == {
        'protocol': "https",
        'subdomain': "",
        'domain': "example.com",
        'port': 443,
        'path': "",
        'query_string': "",
        'anchor': ""
    }

def test_decompose_url_ftp_default_port():
    result = decompose_url("ftp://example.com")
    assert result == {
        'protocol': "ftp",
        'subdomain': "",
        'domain': "example.com",
        'port': 21,
        'path': "",
        'query_string': "",
        'anchor': ""
    }

def test_decompose_url_sftp_default_port():
    result = decompose_url("sftp://example.com")
    assert result == {
        'protocol': "sftp",
        'subdomain': "",
        'domain': "example.com",
        'port': 22,
        'path': "",
        'query_string': "",
        'anchor': ""
    }

def test_decompose_url_query_with_embedded_url():
    result = decompose_url("http://example.com/?next=http://other.com/path")
    # query string should be preserved verbatim
    assert result == {
        'protocol': "http",
        'subdomain': "",
        'domain': "example.com",
        'port': 80,
        'path': "",
        'query_string': "next=http://other.com/path",
        'anchor': ""
    }

def test_decompose_url_invalid_port_with_multiple_colons():
    result = decompose_url("http://foo.com:8080:9090")
    # Expecting rejection message for invalid port
    assert result == "Invalid port: '8080:9090'"
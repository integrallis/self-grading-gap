# test_url_decomposition.py

import pytest
from solution import decompose_url

def test_split_url_with_protocol_and_subdomain():
    # Given "http://foo.bar.com/foobar.html"
    # Protocol = "http"
    # Subdomain = "foo"
    # Domain = "bar.com"
    # Port = 80 (default for http)
    # Path = "foobar.html"
    assert decompose_url("http://foo.bar.com/foobar.html") == {
        "protocol": "http",
        "subdomain": "foo",
        "domain": "bar.com",
        "port": 80,
        "path": "foobar.html",
        "query": "",
        "anchor": ""
    }

def test_split_url_with_explicit_port():
    # Given "https://www.foobar.com:8080/download/install.exe"
    # Protocol = "https"
    # Subdomain = "www"
    # Domain = "foobar.com"
    # Port = 8080 (explicit)
    # Path = "download/install.exe"
    assert decompose_url("https://www.foobar.com:8080/download/install.exe") == {
        "protocol": "https",
        "subdomain": "www",
        "domain": "foobar.com",
        "port": 8080,
        "path": "download/install.exe",
        "query": "",
        "anchor": ""
    }

def test_split_url_with_dotted_host():
    # Given "http://a.b.bar.com/path/to/resource"
    # Protocol = "http"
    # Subdomain = "a.b"
    # Domain = "bar.com"
    # Port = 80 (default for http)
    # Path = "path/to/resource"
    assert decompose_url("http://a.b.bar.com/path/to/resource") == {
        "protocol": "http",
        "subdomain": "a.b",
        "domain": "bar.com",
        "port": 80,
        "path": "path/to/resource",
        "query": "",
        "anchor": ""
    }

def test_split_url_with_localhost():
    # Given "http://localhost:8080/resource"
    # Protocol = "http"
    # Subdomain = ""
    # Domain = "localhost"
    # Port = 8080 (explicit)
    # Path = "resource"
    assert decompose_url("http://localhost:8080/resource") == {
        "protocol": "http",
        "subdomain": "",
        "domain": "localhost",
        "port": 8080,
        "path": "resource",
        "query": "",
        "anchor": ""
    }

def test_split_url_with_no_path():
    # Given "http://example.com/"
    # Protocol = "http"
    # Subdomain = ""
    # Domain = "example.com"
    # Port = 80 (default for http)
    # Path = "" (no path)
    assert decompose_url("http://example.com/") == {
        "protocol": "http",
        "subdomain": "",
        "domain": "example.com",
        "port": 80,
        "path": "",
        "query": "",
        "anchor": ""
    }

def test_split_url_with_empty_path():
    # Given "http://example.com"
    # Protocol = "http"
    # Subdomain = ""
    # Domain = "example.com"
    # Port = 80 (default for http)
    # Path = "" (no path)
    assert decompose_url("http://example.com") == {
        "protocol": "http",
        "subdomain": "",
        "domain": "example.com",
        "port": 80,
        "path": "",
        "query": "",
        "anchor": ""
    }

def test_split_url_with_query_string():
    # Given "http://foo.com/resource?query=string"
    # Protocol = "http"
    # Subdomain = ""
    # Domain = "foo.com"
    # Port = 80 (default for http)
    # Path = "resource"
    # Query = "query=string"
    assert decompose_url("http://foo.com/resource?query=string") == {
        "protocol": "http",
        "subdomain": "",
        "domain": "foo.com",
        "port": 80,
        "path": "resource",
        "query": "query=string",
        "anchor": ""
    }

def test_split_url_with_anchor():
    # Given "http://foo.com/resource#section"
    # Protocol = "http"
    # Subdomain = ""
    # Domain = "foo.com"
    # Port = 80 (default for http)
    # Path = "resource"
    # Anchor = "section"
    assert decompose_url("http://foo.com/resource#section") == {
        "protocol": "http",
        "subdomain": "",
        "domain": "foo.com",
        "port": 80,
        "path": "resource",
        "query": "",
        "anchor": "section"
    }

def test_split_url_with_query_and_anchor():
    # Given "http://foo.com/resource?query=string#section"
    # Protocol = "http"
    # Subdomain = ""
    # Domain = "foo.com"
    # Port = 80 (default for http)
    # Path = "resource"
    # Query = "query=string"
    # Anchor = "section"
    assert decompose_url("http://foo.com/resource?query=string#section") == {
        "protocol": "http",
        "subdomain": "",
        "domain": "foo.com",
        "port": 80,
        "path": "resource",
        "query": "query=string",
        "anchor": "section"
    }

def test_split_url_with_query_directly_after_host():
    # Given "http://foo.com?x=1"
    # Protocol = "http"
    # Subdomain = ""
    # Domain = "foo.com"
    # Port = 80 (default for http)
    # Path = "" (no path)
    # Query = "x=1"
    assert decompose_url("http://foo.com?x=1") == {
        "protocol": "http",
        "subdomain": "",
        "domain": "foo.com",
        "port": 80,
        "path": "",
        "query": "x=1",
        "anchor": ""
    }

def test_split_url_with_embedded_url_in_query():
    # Given "http://foo.com/?next=https://bar.com/a"
    # Protocol = "http"
    # Subdomain = ""
    # Domain = "foo.com"
    # Port = 80 (default for http)
    # Path = ""
    # Query = "next=https://bar.com/a"
    assert decompose_url("http://foo.com/?next=https://bar.com/a") == {
        "protocol": "http",
        "subdomain": "",
        "domain": "foo.com",
        "port": 80,
        "path": "",
        "query": "next=https://bar.com/a",
        "anchor": ""
    }

def test_split_url_with_recognized_tlds():
    # Given "http://example.net"
    # Protocol = "http"
    # Subdomain = ""
    # Domain = "example.net"
    # Port = 80 (default for http)
    # Path = "" (no path)
    assert decompose_url("http://example.net") == {
        "protocol": "http",
        "subdomain": "",
        "domain": "example.net",
        "port": 80,
        "path": "",
        "query": "",
        "anchor": ""
    }
    
def test_split_url_with_recognized_tlds_org():
    # Given "http://example.org"
    # Protocol = "http"
    # Subdomain = ""
    # Domain = "example.org"
    # Port = 80 (default for http)
    assert decompose_url("http://example.org") == {
        "protocol": "http",
        "subdomain": "",
        "domain": "example.org",
        "port": 80,
        "path": "",
        "query": "",
        "anchor": ""
    }

def test_split_url_with_recognized_tlds_int():
    # Given "http://example.int"
    # Protocol = "http"
    # Subdomain = ""
    # Domain = "example.int"
    # Port = 80 (default for http)
    assert decompose_url("http://example.int") == {
        "protocol": "http",
        "subdomain": "",
        "domain": "example.int",
        "port": 80,
        "path": "",
        "query": "",
        "anchor": ""
    }

def test_split_url_with_recognized_tlds_edu():
    # Given "http://example.edu"
    # Protocol = "http"
    # Subdomain = ""
    # Domain = "example.edu"
    # Port = 80 (default for http)
    assert decompose_url("http://example.edu") == {
        "protocol": "http",
        "subdomain": "",
        "domain": "example.edu",
        "port": 80,
        "path": "",
        "query": "",
        "anchor": ""
    }

def test_split_url_with_recognized_tlds_gov():
    # Given "http://example.gov"
    # Protocol = "http"
    # Subdomain = ""
    # Domain = "example.gov"
    # Port = 80 (default for http)
    assert decompose_url("http://example.gov") == {
        "protocol": "http",
        "subdomain": "",
        "domain": "example.gov",
        "port": 80,
        "path": "",
        "query": "",
        "anchor": ""
    }

def test_split_url_with_recognized_tlds_mil():
    # Given "http://example.mil"
    # Protocol = "http"
    # Subdomain = ""
    # Domain = "example.mil"
    # Port = 80 (default for http)
    assert decompose_url("http://example.mil") == {
        "protocol": "http",
        "subdomain": "",
        "domain": "example.mil",
        "port": 80,
        "path": "",
        "query": "",
        "anchor": ""
    }

def test_reject_unsupported_protocol():
    # Given "gopher://example.com"
    # Rejected with message "Unsupported protocol: 'gopher'"
    assert decompose_url("gopher://example.com") == "Unsupported protocol: 'gopher'"

def test_reject_missing_protocol_marker():
    # Given "http//example.com"
    # Rejected with message "Malformed URL, missing '://': 'http//example.com'"
    assert decompose_url("http//example.com") == "Malformed URL, missing '://': 'http//example.com'"

def test_reject_unsupported_top_level_domain():
    # Given "http://example.xyz"
    # Rejected with message "Unsupported top-level domain: 'xyz'"
    assert decompose_url("http://example.xyz") == "Unsupported top-level domain: 'xyz'"

def test_reject_unsupported_top_level_domain_multi_label():
    # Given "http://a.b.example.xyz"
    # Rejected with message "Unsupported top-level domain: 'xyz'"
    assert decompose_url("http://a.b.example.xyz") == "Unsupported top-level domain: 'xyz'"

def test_reject_invalid_port():
    # Given "http://example.com:invalid_port"
    # Rejected with message "Invalid port: 'invalid_port'"
    assert decompose_url("http://example.com:invalid_port") == "Invalid port: 'invalid_port'"

def test_reject_invalid_port_multi_colon():
    # Given "http://foo.com:8080:9090"
    # Rejected with message "Invalid port: '8080:9090'"
    assert decompose_url("http://foo.com:8080:9090") == "Invalid port: '8080:9090'"

def test_reject_missing_host():
    # Given "http:///resource"
    # Rejected with message "Missing host"
    assert decompose_url("http:///resource") == "Missing host"
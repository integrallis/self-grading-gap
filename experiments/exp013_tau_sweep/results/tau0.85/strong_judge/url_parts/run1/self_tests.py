import pytest
from solution import decompose_url

def test_decompose_url_protocol_subdomain_domain_port_path():
    # Test case AC-1.1
    result = decompose_url("http://foo.bar.com/foobar.html")
    assert result["protocol"] == "http" 
    assert result["subdomain"] == "foo" 
    assert result["domain"] == "bar.com" 
    assert result["port"] == 80 
    assert result["path"] == "foobar.html"

    # Test case AC-1.1
    result = decompose_url("https://www.foobar.com:8080/download/install.exe")
    assert result["protocol"] == "https" 
    assert result["subdomain"] == "www" 
    assert result["domain"] == "foobar.com" 
    assert result["port"] == 8080 
    assert result["path"] == "download/install.exe"

def test_decompose_url_subdomain_handling():
    # Test case AC-1.2
    result = decompose_url("http://a.b.bar.com/")
    assert result["subdomain"] == "a.b"  # Host has subdomain "a.b"
    assert result["domain"] == "bar.com"  # Ensure domain is "bar.com"

    # Test case AC-1.3
    result = decompose_url("http://bar.com/")
    assert result["subdomain"] == ""  # No labels before the domain

def test_decompose_url_localhost():
    # Test case AC-1.4
    result = decompose_url("http://localhost:8080/path/to/resource")
    assert result["protocol"] == "http" 
    assert result["subdomain"] == "" 
    assert result["domain"] == "localhost" 
    assert result["port"] == 8080 
    assert result["path"] == "path/to/resource" 

def test_decompose_url_empty_path():
    # Test case AC-1.5
    result = decompose_url("http://example.com")
    assert result["path"] == ""  # No path provided

    result = decompose_url("http://example.com/")
    assert result["path"] == ""  # Bare trailing slash

def test_decompose_url_default_ports():
    # Test case AC-2.1
    result = decompose_url("http://example.com/")
    assert result["port"] == 80  # Default port for http

    result = decompose_url("https://example.com/")
    assert result["port"] == 443  # Default port for https

    result = decompose_url("ftp://example.com/")
    assert result["port"] == 21  # Default port for ftp

    result = decompose_url("sftp://example.com/")
    assert result["port"] == 22  # Default port for sftp

def test_decompose_url_explicit_ports():
    # Test case AC-2.2
    result = decompose_url("http://example.com:8080/")
    assert result["port"] == 8080  # Explicit port overrides default

def test_decompose_url_query_string_anchor():
    # Test case AC-3.1
    result = decompose_url("http://example.com/path?query=1")
    assert result["query"] == "query=1"  # Query string captured
    assert result["path"] == "path"  # Ensure path excludes query text

    # Test case AC-3.2
    result = decompose_url("http://example.com/path#anchor")
    assert result["anchor"] == "anchor"  # Anchor captured
    assert result["path"] == "path"  # Ensure path excludes anchor text

    # Test case AC-3.3
    result = decompose_url("http://example.com/path?query=1#anchor")
    assert result["query"] == "query=1"  # Both query and anchor present
    assert result["anchor"] == "anchor"
    assert result["path"] == "path"  # Ensure path excludes both query and anchor

    # Test case AC-3.4
    result = decompose_url("http://example.com?query=1")
    assert result["path"] == ""  # Path is empty

    # Test case AC-3.5
    result = decompose_url("http://example.com/path?query=http://another-url")
    assert result["query"] == "query=http://another-url"  # Full URL in query

def test_decompose_url_reject_unsupported_protocol():
    # Test case AC-4.1
    with pytest.raises(ValueError) as exc:
        decompose_url("gopher://example.com")
    assert str(exc.value) == "Unsupported protocol: 'gopher'"

def test_decompose_url_reject_missing_marker():
    # Test case AC-4.2
    with pytest.raises(ValueError) as exc:
        decompose_url("example.com")
    assert str(exc.value) == "Malformed URL, missing '://': 'example.com'"

def test_decompose_url_reject_invalid_top_level_domain():
    # Test case AC-4.3
    with pytest.raises(ValueError) as exc:
        decompose_url("http://example.invalid/")
    assert str(exc.value) == "Unsupported top-level domain: 'invalid'"

    # Additional test for multi-label host with invalid TLD
    with pytest.raises(ValueError) as exc:
        decompose_url("http://foo.bar.invalid/")
    assert str(exc.value) == "Unsupported top-level domain: 'invalid'"

def test_decompose_url_reject_invalid_port():
    # Test case AC-4.4
    with pytest.raises(ValueError) as exc:
        decompose_url("http://example.com:invalid/")
    assert str(exc.value) == "Invalid port: 'invalid'"

    # Test case for explicit "everything after the first colon"
    with pytest.raises(ValueError) as exc:
        decompose_url("http://foo.com:8080:9090/")
    assert str(exc.value) == "Invalid port: '8080:9090'"

def test_decompose_url_reject_missing_host():
    # Test case AC-4.5
    with pytest.raises(ValueError) as exc:
        decompose_url("http:///path")
    assert str(exc.value) == "Missing host"

def test_decompose_url_recognized_tlds():
    # Test cases for recognized TLDs
    for tld in ["net", "org", "int", "edu", "gov", "mil"]:
        result = decompose_url(f"http://foo.bar.{tld}/")
        assert result["domain"] == f"bar.{tld}"  # Ensure domain is correctly parsed
        assert result["subdomain"] == "foo"  # Ensure subdomain is "foo"

    # Additional test for a URL with a subdomain, path, query, and anchor
    result = decompose_url("http://foo.example.com/path/to/page?x=1#section")
    assert result["subdomain"] == "foo"
    assert result["domain"] == "example.com"
    assert result["path"] == "path/to/page"
    assert result["query"] == "x=1"
    assert result["anchor"] == "section"
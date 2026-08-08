import pytest
from solution import decompose_url

def test_decompose_url_protocol_subdomain_domain_port_path():
    # AC-1.1: "http://foo.bar.com/foobar.html" => protocol "http", subdomain "foo", domain "bar.com", port 80, path "foobar.html"
    assert decompose_url("http://foo.bar.com/foobar.html") == ("http", "foo", "bar.com", 80, "foobar.html", "", "")
    
    # AC-1.1: "https://www.foobar.com:8080/download/install.exe" => protocol "https", subdomain "www", domain "foobar.com", port 8080, path "download/install.exe"
    assert decompose_url("https://www.foobar.com:8080/download/install.exe") == ("https", "www", "foobar.com", 8080, "download/install.exe", "", "")

def test_decompose_url_subdomain_cases():
    # AC-1.2: "http://a.b.bar.com" => subdomain "a.b", domain "bar.com"
    assert decompose_url("http://a.b.bar.com") == ("http", "a.b", "bar.com", 80, "", "", "")
    
    # AC-1.3: "http://bar.com" => empty subdomain
    assert decompose_url("http://bar.com") == ("http", "", "bar.com", 80, "", "", "")
    
    # AC-1.4: "http://localhost:8080/status" => empty subdomain, domain "localhost", port 8080, path "status"
    assert decompose_url("http://localhost:8080/status") == ("http", "", "localhost", 8080, "status", "", "")
    
    # AC-1.5: "http://example.com/" => empty path
    assert decompose_url("http://example.com/") == ("http", "", "example.com", 80, "", "", "")
    
    # AC-1.5: "http://example.com" => empty path
    assert decompose_url("http://example.com") == ("http", "", "example.com", 80, "", "", "")

def test_decompose_url_top_level_domains():
    # AC-1.6: "http://foo.bar.com" => valid TLD
    assert decompose_url("http://foo.bar.com") == ("http", "foo", "bar.com", 80, "", "", "")
    
    # AC-1.6: "http://foo.bar.net" => valid TLD
    assert decompose_url("http://foo.bar.net") == ("http", "foo", "bar.net", 80, "", "", "")
    
    # AC-1.6: "http://foo.bar.org" => valid TLD
    assert decompose_url("http://foo.bar.org") == ("http", "foo", "bar.org", 80, "", "", "")
    
    # AC-1.6: "http://foo.bar.edu" => valid TLD
    assert decompose_url("http://foo.bar.edu") == ("http", "foo", "bar.edu", 80, "", "", "")
    
    # AC-1.6: "http://foo.bar.gov" => valid TLD
    assert decompose_url("http://foo.bar.gov") == ("http", "foo", "bar.gov", 80, "", "", "")
    
    # AC-1.6: "http://foo.bar.mil" => valid TLD
    assert decompose_url("http://foo.bar.mil") == ("http", "foo", "bar.mil", 80, "", "", "")
    
    # AC-1.6: "http://foo.bar.int" => valid TLD
    assert decompose_url("http://foo.bar.int") == ("http", "foo", "bar.int", 80, "", "", "")
    
    # AC-4.3: "http://foo.bar.xyz" => unsupported TLD
    with pytest.raises(Exception) as exc_info:
        decompose_url("http://foo.bar.xyz")
    assert str(exc_info.value) == "Unsupported top-level domain: 'xyz'"

def test_decompose_url_ports():
    # AC-2.1: "http://example.com" => default port 80
    assert decompose_url("http://example.com") == ("http", "", "example.com", 80, "", "", "")
    
    # AC-2.1: "https://example.com" => default port 443
    assert decompose_url("https://example.com") == ("https", "", "example.com", 443, "", "", "")
    
    # AC-2.1: "ftp://example.com" => default port 21
    assert decompose_url("ftp://example.com") == ("ftp", "", "example.com", 21, "", "", "")
    
    # AC-2.1: "sftp://example.com" => default port 22
    assert decompose_url("sftp://example.com") == ("sftp", "", "example.com", 22, "", "", "")
    
    # AC-2.2: "http://example.com:90" => explicit port 90
    assert decompose_url("http://example.com:90") == ("http", "", "example.com", 90, "", "", "")

def test_decompose_url_query_string_and_anchor():
    # AC-3.1: "http://example.com?search=test" => query "search=test"
    assert decompose_url("http://example.com?search=test") == ("http", "", "example.com", 80, "", "search=test", "")
    
    # AC-3.2: "http://example.com#section1" => anchor "section1"
    assert decompose_url("http://example.com#section1") == ("http", "", "example.com", 80, "", "", "section1")
    
    # AC-3.3: "http://www.example.com/a/b?x=1#frag" => path "a/b", query "x=1", anchor "frag"
    assert decompose_url("http://www.example.com/a/b?x=1#frag") == ("http", "www", "example.com", 80, "a/b", "x=1", "frag")
    
    # AC-3.4: "http://example.com?search=test" => empty path
    assert decompose_url("http://example.com?search=test") == ("http", "", "example.com", 80, "", "search=test", "")
    
    # AC-3.5: "http://example.com?search=http://another.com" => query includes a URL
    assert decompose_url("http://example.com?search=http://another.com") == ("http", "", "example.com", 80, "", "search=http://another.com", "")

def test_decompose_url_reject_invalid_urls():
    # AC-4.1: "gopher://example.com" => unsupported protocol
    with pytest.raises(Exception) as exc_info:
        decompose_url("gopher://example.com")
    assert str(exc_info.value) == "Unsupported protocol: 'gopher'"
    
    # AC-4.2: "example.com" => missing "://"
    with pytest.raises(Exception) as exc_info:
        decompose_url("example.com")
    assert str(exc_info.value) == "Malformed URL, missing '://': 'example.com'"
    
    # AC-4.4: "http://example.com:abc" => invalid port
    with pytest.raises(Exception) as exc_info:
        decompose_url("http://example.com:abc")
    assert str(exc_info.value) == "Invalid port: 'abc'"
    
    # AC-4.4: "http://foo.com:8080:9090" => multi-colon invalid port
    with pytest.raises(Exception) as exc_info:
        decompose_url("http://foo.com:8080:9090")
    assert str(exc_info.value) == "Invalid port: '8080:9090'"
    
    # AC-4.5: "http://:80/path" => missing host
    with pytest.raises(Exception) as exc_info:
        decompose_url("http://:80/path")
    assert str(exc_info.value) == "Missing host"
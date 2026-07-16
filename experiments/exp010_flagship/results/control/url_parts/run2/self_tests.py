from solution import decompose_url

def test_decompose_url_protocol_subdomain_domain_port_path():
    # AC-1.1: http://foo.bar.com/foobar.html
    result = decompose_url("http://foo.bar.com/foobar.html")
    assert result == {
        "protocol": "http", 
        "subdomain": "foo", 
        "domain": "bar.com", 
        "port": 80, 
        "path": "foobar.html", 
        "query": "", 
        "anchor": ""
    }
    
    # AC-1.1: https://www.foobar.com:8080/download/install.exe
    result = decompose_url("https://www.foobar.com:8080/download/install.exe")
    assert result == {
        "protocol": "https", 
        "subdomain": "www", 
        "domain": "foobar.com", 
        "port": 8080, 
        "path": "download/install.exe", 
        "query": "", 
        "anchor": ""
    }

def test_decompose_url_subdomain_and_domain():
    # AC-1.2: a.b.bar.com
    result = decompose_url("http://a.b.bar.com")
    assert result == {
        "protocol": "http", 
        "subdomain": "a.b", 
        "domain": "bar.com", 
        "port": 80, 
        "path": "", 
        "query": "", 
        "anchor": ""
    }

    # AC-1.3: bar.com
    result = decompose_url("http://bar.com")
    assert result == {
        "protocol": "http", 
        "subdomain": "", 
        "domain": "bar.com", 
        "port": 80, 
        "path": "", 
        "query": "", 
        "anchor": ""
    }

def test_decompose_url_localhost():
    # AC-1.4: localhost
    result = decompose_url("http://localhost:8080/path")
    assert result == {
        "protocol": "http", 
        "subdomain": "", 
        "domain": "localhost", 
        "port": 8080, 
        "path": "path", 
        "query": "", 
        "anchor": ""
    }

def test_decompose_url_empty_path():
    # AC-1.5: no path
    result = decompose_url("http://example.com")
    assert result == {
        "protocol": "http", 
        "subdomain": "", 
        "domain": "example.com", 
        "port": 80, 
        "path": "", 
        "query": "", 
        "anchor": ""
    }

    # AC-1.5: trailing slash
    result = decompose_url("http://example.com/")
    assert result == {
        "protocol": "http", 
        "subdomain": "", 
        "domain": "example.com", 
        "port": 80, 
        "path": "", 
        "query": "", 
        "anchor": ""
    }

def test_decompose_url_recognized_tld():
    # AC-1.6: .com
    result = decompose_url("http://example.com")
    assert result == {
        "protocol": "http", 
        "subdomain": "", 
        "domain": "example.com", 
        "port": 80, 
        "path": "", 
        "query": "", 
        "anchor": ""
    }

    # AC-4.3: Unsupported TLD
    with pytest.raises(ValueError) as excinfo:
        decompose_url("http://example.xyz")
    assert str(excinfo.value) == "Unsupported top-level domain: 'xyz'"

def test_decompose_url_default_ports():
    # AC-2.1: http without port
    result = decompose_url("http://example.com")
    assert result["port"] == 80
    
    # AC-2.1: https without port
    result = decompose_url("https://example.com")
    assert result["port"] == 443

def test_decompose_url_explicit_ports():
    # AC-2.2: explicit port 8080
    result = decompose_url("http://example.com:8080")
    assert result["port"] == 8080

def test_decompose_url_query_and_anchor():
    # AC-3.1: query string
    result = decompose_url("http://example.com?query=1")
    assert result["query"] == "query=1"
    assert result["path"] == ""

    # AC-3.2: anchor
    result = decompose_url("http://example.com#section")
    assert result["anchor"] == "section"
    assert result["path"] == ""

    # AC-3.3: both query and anchor
    result = decompose_url("http://example.com/path?query=1#section")
    assert result["query"] == "query=1"
    assert result["anchor"] == "section"

    # AC-3.4: query follows host directly
    result = decompose_url("http://example.com?query=1")
    assert result["path"] == ""

def test_decompose_url_malformed_urls():
    # AC-4.2: missing '://'
    with pytest.raises(ValueError) as excinfo:
        decompose_url("http/example.com")
    assert str(excinfo.value) == "Malformed URL, missing '://': 'http/example.com'"

    # AC-4.4: invalid port
    with pytest.raises(ValueError) as excinfo:
        decompose_url("http://example.com:abc")
    assert str(excinfo.value) == "Invalid port: 'abc'"

    # AC-4.5: missing host
    with pytest.raises(ValueError) as excinfo:
        decompose_url("http://:80/path")
    assert str(excinfo.value) == "Missing host"
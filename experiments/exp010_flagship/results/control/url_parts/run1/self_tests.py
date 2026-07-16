from solution import decompose_url

def test_split_url_protocol_subdomain_domain_port_path():
    # AC-1.1
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

def test_subdomain_and_domain():
    # AC-1.2
    result = decompose_url("http://a.b.bar.com")
    assert result["subdomain"] == "a.b"
    assert result["domain"] == "bar.com"

    # AC-1.3
    result = decompose_url("http://bar.com")
    assert result["subdomain"] == ""
    assert result["domain"] == "bar.com"

def test_localhost():
    # AC-1.4
    result = decompose_url("http://localhost:8080/path")
    assert result["subdomain"] == ""
    assert result["domain"] == "localhost"
    assert result["port"] == 8080
    assert result["path"] == "path"

def test_empty_path():
    # AC-1.5
    result = decompose_url("http://foo.bar.com")
    assert result["path"] == ""

    result = decompose_url("http://foo.bar.com/")
    assert result["path"] == ""

def test_top_level_domains():
    # AC-1.6
    result = decompose_url("http://example.com")
    assert result["domain"] == "example.com"

def test_apply_default_ports():
    # AC-2.1
    result = decompose_url("http://example.com")
    assert result["port"] == 80

    result = decompose_url("https://example.com")
    assert result["port"] == 443

    result = decompose_url("ftp://example.com")
    assert result["port"] == 21

    result = decompose_url("sftp://example.com")
    assert result["port"] == 22

def test_override_default_ports():
    # AC-2.2
    result = decompose_url("http://example.com:8080")
    assert result["port"] == 8080

def test_capture_query_string_and_anchor():
    # AC-3.1
    result = decompose_url("http://example.com/path?query=1")
    assert result["query"] == "query=1"
    assert result["path"] == "path"

    # AC-3.2
    result = decompose_url("http://example.com/path#anchor")
    assert result["anchor"] == "anchor"
    assert result["path"] == "path"

    # AC-3.3
    result = decompose_url("http://example.com/path?query=1#anchor")
    assert result["query"] == "query=1"
    assert result["anchor"] == "anchor"

    # AC-3.4
    result = decompose_url("http://example.com?query=1")
    assert result["path"] == ""

def test_full_url_in_query_string():
    # AC-3.5
    result = decompose_url("http://example.com?url=http://another.com")
    assert result["query"] == "url=http://another.com"

def test_reject_unsupported_protocol():
    # AC-4.1
    with pytest.raises(ValueError) as excinfo:
        decompose_url("gopher://example.com")
    assert str(excinfo.value) == "Unsupported protocol: 'gopher'"

def test_reject_missing_ternary():
    # AC-4.2
    with pytest.raises(ValueError) as excinfo:
        decompose_url("http:/example.com")
    assert str(excinfo.value) == "Malformed URL, missing '://': 'http:/example.com'"

def test_reject_unsupported_tld():
    # AC-4.3
    with pytest.raises(ValueError) as excinfo:
        decompose_url("http://example.xyz")
    assert str(excinfo.value) == "Unsupported top-level domain: 'xyz'"

def test_reject_invalid_port():
    # AC-4.4
    with pytest.raises(ValueError) as excinfo:
        decompose_url("http://example.com:80abc")
    assert str(excinfo.value) == "Invalid port: '80abc'"

def test_reject_missing_host():
    # AC-4.5
    with pytest.raises(ValueError) as excinfo:
        decompose_url("http://")
    assert str(excinfo.value) == "Missing host"
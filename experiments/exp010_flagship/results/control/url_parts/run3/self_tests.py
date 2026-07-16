from solution import decompose_url

def test_decompose_url_protocol_subdomain_domain_path():
    # AC-1.1
    assert decompose_url("http://foo.bar.com/foobar.html") == {
        "protocol": "http",
        "subdomain": "foo",
        "domain": "bar.com",
        "port": 80,
        "path": "foobar.html",
        "query": "",
        "anchor": ""
    }
    
    # AC-1.1
    assert decompose_url("https://www.foobar.com:8080/download/install.exe") == {
        "protocol": "https",
        "subdomain": "www",
        "domain": "foobar.com",
        "port": 8080,
        "path": "download/install.exe",
        "query": "",
        "anchor": ""
    }
    
    # AC-1.2
    assert decompose_url("http://a.b.bar.com/path") == {
        "protocol": "http",
        "subdomain": "a.b",
        "domain": "bar.com",
        "port": 80,
        "path": "path",
        "query": "",
        "anchor": ""
    }
    
    # AC-1.3
    assert decompose_url("http://bar.com/path") == {
        "protocol": "http",
        "subdomain": "",
        "domain": "bar.com",
        "port": 80,
        "path": "path",
        "query": "",
        "anchor": ""
    }
    
    # AC-1.4
    assert decompose_url("http://localhost:8080/path") == {
        "protocol": "http",
        "subdomain": "",
        "domain": "localhost",
        "port": 8080,
        "path": "path",
        "query": "",
        "anchor": ""
    }
    
    # AC-1.5
    assert decompose_url("http://example.com/") == {
        "protocol": "http",
        "subdomain": "",
        "domain": "example.com",
        "port": 80,
        "path": "",
        "query": "",
        "anchor": ""
    }
    
    # AC-1.5
    assert decompose_url("http://example.com") == {
        "protocol": "http",
        "subdomain": "",
        "domain": "example.com",
        "port": 80,
        "path": "",
        "query": "",
        "anchor": ""
    }
    
    # AC-1.6
    assert decompose_url("http://example.xyz/path") == {
        "protocol": "http",
        "subdomain": "",
        "domain": "example.xyz",
        "port": 80,
        "path": "path",
        "query": "",
        "anchor": ""
    }

def test_decompose_url_ports():
    # AC-2.1
    assert decompose_url("http://example.com/path") == {
        "protocol": "http",
        "subdomain": "",
        "domain": "example.com",
        "port": 80,
        "path": "path",
        "query": "",
        "anchor": ""
    }
    
    # AC-2.1
    assert decompose_url("https://example.com/path") == {
        "protocol": "https",
        "subdomain": "",
        "domain": "example.com",
        "port": 443,
        "path": "path",
        "query": "",
        "anchor": ""
    }
    
    # AC-2.2
    assert decompose_url("ftp://example.com:21/path") == {
        "protocol": "ftp",
        "subdomain": "",
        "domain": "example.com",
        "port": 21,
        "path": "path",
        "query": "",
        "anchor": ""
    }
    
    # AC-2.2
    assert decompose_url("sftp://example.com:2222/path") == {
        "protocol": "sftp",
        "subdomain": "",
        "domain": "example.com",
        "port": 2222,
        "path": "path",
        "query": "",
        "anchor": ""
    }

def test_decompose_url_query_and_anchor():
    # AC-3.1
    assert decompose_url("http://example.com/path?query=1") == {
        "protocol": "http",
        "subdomain": "",
        "domain": "example.com",
        "port": 80,
        "path": "path",
        "query": "query=1",
        "anchor": ""
    }
    
    # AC-3.2
    assert decompose_url("http://example.com/path#anchor") == {
        "protocol": "http",
        "subdomain": "",
        "domain": "example.com",
        "port": 80,
        "path": "path",
        "query": "",
        "anchor": "anchor"
    }
    
    # AC-3.3
    assert decompose_url("http://example.com/path?query=1#anchor") == {
        "protocol": "http",
        "subdomain": "",
        "domain": "example.com",
        "port": 80,
        "path": "path",
        "query": "query=1",
        "anchor": "anchor"
    }
    
    # AC-3.4
    assert decompose_url("http://example.com?query=1") == {
        "protocol": "http",
        "subdomain": "",
        "domain": "example.com",
        "port": 80,
        "path": "",
        "query": "query=1",
        "anchor": ""
    }
    
    # AC-3.5
    assert decompose_url("http://example.com/path?http://another.com") == {
        "protocol": "http",
        "subdomain": "",
        "domain": "example.com",
        "port": 80,
        "path": "path",
        "query": "http://another.com",
        "anchor": ""
    }

def test_decompose_url_rejects():
    # AC-4.1
    try:
        decompose_url("gopher://example.com")
    except ValueError as e:
        assert str(e) == "Unsupported protocol: 'gopher'"
    
    # AC-4.2
    try:
        decompose_url("http://example.com")
    except ValueError as e:
        assert str(e) == "Malformed URL, missing '://': 'http://example.com'"
    
    # AC-4.3
    try:
        decompose_url("http://example.xyz/path")
    except ValueError as e:
        assert str(e) == "Unsupported top-level domain: 'xyz'"
    
    # AC-4.4
    try:
        decompose_url("http://example.com:notaport/path")
    except ValueError as e:
        assert str(e) == "Invalid port: 'notaport'"
    
    # AC-4.5
    try:
        decompose_url("http://:8080/path")
    except ValueError as e:
        assert str(e) == "Missing host"
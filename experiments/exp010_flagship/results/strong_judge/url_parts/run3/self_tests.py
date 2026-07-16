import pytest
from solution import decompose_url

def test_decompose_url_http_example():
    # Given: "http://foo.bar.com/foobar.html"
    # Expected: protocol "http", subdomain "foo", domain "bar.com", port 80, path "foobar.html"
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

def test_decompose_url_https_example():
    # Given: "https://www.foobar.com:8080/download/install.exe"
    # Expected: protocol "https", subdomain "www", domain "foobar.com", port 8080, path "download/install.exe"
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

def test_decompose_url_subdomain_example():
    # Given: "http://a.b.bar.com/foobar.html"
    # Expected: protocol "http", subdomain "a.b", domain "bar.com", port 80, path "foobar.html"
    result = decompose_url("http://a.b.bar.com/foobar.html")
    assert result == {
        "protocol": "http",
        "subdomain": "a.b",
        "domain": "bar.com",
        "port": 80,
        "path": "foobar.html",
        "query": "",
        "anchor": ""
    }

def test_decompose_url_empty_subdomain():
    # Given: "http://bar.com/foobar.html"
    # Expected: protocol "http", subdomain "", domain "bar.com", port 80, path "foobar.html"
    result = decompose_url("http://bar.com/foobar.html")
    assert result == {
        "protocol": "http",
        "subdomain": "",
        "domain": "bar.com",
        "port": 80,
        "path": "foobar.html",
        "query": "",
        "anchor": ""
    }

def test_decompose_url_localhost():
    # Given: "http://localhost:8080/path/to/resource"
    # Expected: protocol "http", subdomain "", domain "localhost", port 8080, path "path/to/resource"
    result = decompose_url("http://localhost:8080/path/to/resource")
    assert result == {
        "protocol": "http",
        "subdomain": "",
        "domain": "localhost",
        "port": 8080,
        "path": "path/to/resource",
        "query": "",
        "anchor": ""
    }

def test_decompose_url_no_path():
    # Given: "http://bar.com"
    # Expected: protocol "http", subdomain "", domain "bar.com", port 80, path ""
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

def test_decompose_url_bare_trailing_slash():
    # Given: "http://bar.com/"
    # Expected: protocol "http", subdomain "", domain "bar.com", port 80, path ""
    result = decompose_url("http://bar.com/")
    assert result == {
        "protocol": "http",
        "subdomain": "",
        "domain": "bar.com",
        "port": 80,
        "path": "",
        "query": "",
        "anchor": ""
    }

def test_decompose_url_ftp_default_port():
    # Given: "ftp://example.com/path"
    # Expected: protocol "ftp", subdomain "", domain "example.com", port 21, path "path"
    result = decompose_url("ftp://example.com/path")
    assert result == {
        "protocol": "ftp",
        "subdomain": "",
        "domain": "example.com",
        "port": 21,
        "path": "path",
        "query": "",
        "anchor": ""
    }

def test_decompose_url_https_default_port():
    # Given: "https://example.com/path"
    # Expected: protocol "https", subdomain "", domain "example.com", port 443, path "path"
    result = decompose_url("https://example.com/path")
    assert result == {
        "protocol": "https",
        "subdomain": "",
        "domain": "example.com",
        "port": 443,
        "path": "path",
        "query": "",
        "anchor": ""
    }

def test_decompose_url_sftp_default_port():
    # Given: "sftp://example.com/path"
    # Expected: protocol "sftp", subdomain "", domain "example.com", port 22, path "path"
    result = decompose_url("sftp://example.com/path")
    assert result == {
        "protocol": "sftp",
        "subdomain": "",
        "domain": "example.com",
        "port": 22,
        "path": "path",
        "query": "",
        "anchor": ""
    }

def test_decompose_url_with_query():
    # Given: "http://foo.com?search=query"
    # Expected: protocol "http", subdomain "", domain "foo.com", port 80, path "", query "search=query"
    result = decompose_url("http://foo.com?search=query")
    assert result == {
        "protocol": "http",
        "subdomain": "",
        "domain": "foo.com",
        "port": 80,
        "path": "",
        "query": "search=query",
        "anchor": ""
    }

def test_decompose_url_with_anchor():
    # Given: "http://example.com#section"
    # Expected: protocol "http", subdomain "", domain "example.com", port 80, path "", query "", anchor "section"
    result = decompose_url("http://example.com#section")
    assert result == {
        "protocol": "http",
        "subdomain": "",
        "domain": "example.com",
        "port": 80,
        "path": "",
        "query": "",
        "anchor": "section"
    }

def test_decompose_url_with_query_and_anchor():
    # Given: "http://www.example.com/page?x=1#top"
    # Expected: protocol "http", subdomain "www", domain "example.com", port 80, path "page", query "x=1", anchor "top"
    result = decompose_url("http://www.example.com/page?x=1#top")
    assert result == {
        "protocol": "http",
        "subdomain": "www",
        "domain": "example.com",
        "port": 80,
        "path": "page",
        "query": "x=1",
        "anchor": "top"
    }

def test_decompose_url_query_only():
    # Given: "http://example.com?search=query"
    # Expected: protocol "http", subdomain "", domain "example.com", port 80, path "", query "search=query"
    result = decompose_url("http://example.com?search=query")
    assert result == {
        "protocol": "http",
        "subdomain": "",
        "domain": "example.com",
        "port": 80,
        "path": "",
        "query": "search=query",
        "anchor": ""
    }

def test_decompose_url_anchor_only():
    # Given: "http://example.com#section"
    # Expected: protocol "http", subdomain "", domain "example.com", port 80, path "", query "", anchor "section"
    result = decompose_url("http://example.com#section")
    assert result == {
        "protocol": "http",
        "subdomain": "",
        "domain": "example.com",
        "port": 80,
        "path": "",
        "query": "",
        "anchor": "section"
    }

def test_decompose_url_unsupported_protocol():
    # Given: "gopher://example.com"
    # Expected: "Unsupported protocol: 'gopher'"
    with pytest.raises(Exception) as exc:
        decompose_url("gopher://example.com")
    assert str(exc.value) == "Unsupported protocol: 'gopher'"

def test_decompose_url_missing_protocol():
    # Given: "example.com"
    # Expected: "Malformed URL, missing '://': 'example.com'"
    with pytest.raises(Exception) as exc:
        decompose_url("example.com")
    assert str(exc.value) == "Malformed URL, missing '://': 'example.com'"

def test_decompose_url_unsupported_tld():
    # Given: "http://example.xyz"
    # Expected: "Unsupported top-level domain: 'xyz'"
    with pytest.raises(Exception) as exc:
        decompose_url("http://example.xyz")
    assert str(exc.value) == "Unsupported top-level domain: 'xyz'"

def test_decompose_url_unsupported_tld_multi_label():
    # Given: "http://a.b.example.xyz"
    # Expected: "Unsupported top-level domain: 'xyz'"
    with pytest.raises(Exception) as exc:
        decompose_url("http://a.b.example.xyz")
    assert str(exc.value) == "Unsupported top-level domain: 'xyz'"

def test_decompose_url_invalid_port():
    # Given: "http://example.com:abc"
    # Expected: "Invalid port: 'abc'"
    with pytest.raises(Exception) as exc:
        decompose_url("http://example.com:abc")
    assert str(exc.value) == "Invalid port: 'abc'"

def test_decompose_url_invalid_port_multiple():
    # Given: "http://example.com:8080:9090"
    # Expected: "Invalid port: '8080:9090'"
    with pytest.raises(Exception) as exc:
        decompose_url("http://example.com:8080:9090")
    assert str(exc.value) == "Invalid port: '8080:9090'"

def test_decompose_url_missing_host():
    # Given: "http:///path"
    # Expected: "Missing host"
    with pytest.raises(Exception) as exc:
        decompose_url("http:///path")
    assert str(exc.value) == "Missing host"

def test_decompose_url_with_embedded_url_in_query():
    # Given: "http://example.com/path?next=https://a.b.com/x"
    # Expected: query "next=https://a.b.com/x"
    result = decompose_url("http://example.com/path?next=https://a.b.com/x")
    assert result == {
        "protocol": "http",
        "subdomain": "",
        "domain": "example.com",
        "port": 80,
        "path": "path",
        "query": "next=https://a.b.com/x",
        "anchor": ""
    }
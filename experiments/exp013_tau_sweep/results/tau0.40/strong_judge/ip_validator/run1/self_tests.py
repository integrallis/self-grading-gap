from solution import validate_ipv4_address

def test_accept_valid_host_addresses():
    # 1.1.1.1 is a valid address
    assert validate_ipv4_address("1.1.1.1") == True
    # 192.168.1.1 is a valid address
    assert validate_ipv4_address("192.168.1.1") == True
    # 10.0.0.1 is a valid address
    assert validate_ipv4_address("10.0.0.1") == True
    # 127.0.0.1 is a valid address
    assert validate_ipv4_address("127.0.0.1") == True
    # 0.1.1.1 is valid, since zero is acceptable in the first position
    assert validate_ipv4_address("0.1.1.1") == True
    # 255.255.255.1 is valid, as 255 is acceptable in the first three positions
    assert validate_ipv4_address("255.255.255.1") == True

def test_reject_invalid_malformed_text():
    # No octets (empty string)
    assert validate_ipv4_address("") == False
    # Three octets
    assert validate_ipv4_address("192.168.1") == False
    # Five octets
    assert validate_ipv4_address("192.168.1.1.1") == False
    # Extra dot at the end
    assert validate_ipv4_address("192.168.1.1.") == False
    # Doubled dot (empty octet)
    assert validate_ipv4_address("192.168..1") == False
    # Leading or trailing whitespace
    assert validate_ipv4_address(" 192.168.1.1") == False
    assert validate_ipv4_address("192.168.1.1 ") == False
    # Non-digit characters
    assert validate_ipv4_address("192.168.a.1") == False
    assert validate_ipv4_address("192.168.1.-1") == False
    assert validate_ipv4_address("192.168.1.01") == False  # Leading zero
    assert validate_ipv4_address("192.168.1.+1") == False  # Plus sign
    assert validate_ipv4_address("192.168.A.1") == False  # Uppercase letter

def test_enforce_octet_values():
    # Octet greater than 255
    assert validate_ipv4_address("256.0.0.1") == False
    assert validate_ipv4_address("1.256.0.1") == False
    assert validate_ipv4_address("1.1.256.1") == False
    assert validate_ipv4_address("1.1.1.256") == False
    
    # Leading zero in octets
    assert validate_ipv4_address("01.1.1.1") == False
    assert validate_ipv4_address("1.01.1.1") == False
    assert validate_ipv4_address("1.1.01.1") == False
    assert validate_ipv4_address("1.1.1.01") == False

def test_require_host_assignable_final_octet():
    # Final octet is 0 (network address)
    assert validate_ipv4_address("192.168.1.0") == False
    assert validate_ipv4_address("0.0.0.0") == False  # 0.0.0.0 included
    
    # Final octet is 255 (broadcast address)
    assert validate_ipv4_address("192.168.1.255") == False
    assert validate_ipv4_address("255.255.255.255") == False  # 255.255.255.255 included
    
    # Valid final octet
    assert validate_ipv4_address("192.168.1.1") == True
    assert validate_ipv4_address("192.168.1.254") == True
from solution import validate_ipv4_address

def test_accept_well_formed_host_addresses():
    # Valid addresses
    assert validate_ipv4_address("1.1.1.1") == True  # Valid host address
    assert validate_ipv4_address("192.168.1.1") == True  # Valid host address
    assert validate_ipv4_address("10.0.0.1") == True  # Valid host address
    assert validate_ipv4_address("127.0.0.1") == True  # Valid host address
    assert validate_ipv4_address("192.168.1.254") == True  # Valid host address
    assert validate_ipv4_address("0.1.1.1") == True  # Valid host address (0 in non-final position)
    assert validate_ipv4_address("255.1.1.1") == True  # Valid host address (255 in non-final position)
    assert validate_ipv4_address("1.255.1.1") == True  # Valid host address (255 in non-final position)
    assert validate_ipv4_address("1.1.255.1") == True  # Valid host address (255 in non-final position)

def test_reject_malformed_text():
    # Invalid addresses
    assert validate_ipv4_address("1.1.1") == False  # Only three octets
    assert validate_ipv4_address("1.1.1.1.1") == False  # Five octets
    assert validate_ipv4_address("") == False  # Empty string
    assert validate_ipv4_address("1..1.1.1") == False  # Empty octet due to double dot
    assert validate_ipv4_address("1.1.1.") == False  # Empty octet due to trailing dot
    assert validate_ipv4_address("1.1.1.01") == False  # Leading zero in last octet
    assert validate_ipv4_address("+1.1.1.1") == False  # Signed octet
    assert validate_ipv4_address("-1.1.1.1") == False  # Signed octet
    assert validate_ipv4_address(" 1.1.1.1") == False  # Leading whitespace
    assert validate_ipv4_address("1.1.1.1 ") == False  # Trailing whitespace
    assert validate_ipv4_address("a.1.1.1") == False  # Lowercase letter in octet
    assert validate_ipv4_address("A.1.1.1") == False  # Uppercase letter in octet

def test_enforce_octet_values():
    # Invalid octet values
    assert validate_ipv4_address("256.1.1.1") == False  # Octet greater than 255
    assert validate_ipv4_address("1.256.1.1") == False  # Octet greater than 255 in middle position
    assert validate_ipv4_address("1.1.256.1") == False  # Octet greater than 255 in middle position
    assert validate_ipv4_address("1.01.1.1") == False  # Leading zero in octet
    assert validate_ipv4_address("01.1.1.1") == False  # Leading zero in first octet
    assert validate_ipv4_address("1.1.01.1") == False  # Leading zero in third octet
    assert validate_ipv4_address("1.1.1.1.") == False  # Trailing dot with no octet
    assert validate_ipv4_address("1.1.1.256") == False  # Final octet greater than 255

def test_require_host_assignable_final_octet():
    # Invalid final octet values
    assert validate_ipv4_address("0.0.0.0") == False  # Network address
    assert validate_ipv4_address("192.168.0.0") == False  # Network address
    assert validate_ipv4_address("255.255.255.255") == False  # Broadcast address
    assert validate_ipv4_address("192.168.1.255") == False  # Broadcast address
    assert validate_ipv4_address("192.168.1.0") == False  # Network address
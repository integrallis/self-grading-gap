from solution import validate_ipv4_address

def test_accept_well_formed_host_addresses():
    assert validate_ipv4_address("1.1.1.1") == True  # Valid host address
    assert validate_ipv4_address("192.168.1.1") == True  # Valid host address
    assert validate_ipv4_address("10.0.0.1") == True  # Valid host address
    assert validate_ipv4_address("127.0.0.1") == True  # Valid host address
    assert validate_ipv4_address("0.1.1.1") == True  # 0 is allowed in the first position
    assert validate_ipv4_address("255.255.255.1") == True  # 255 is allowed in the first three positions

def test_reject_malformed_text():
    assert validate_ipv4_address("1.1.1") == False  # Only three octets
    assert validate_ipv4_address("1.1.1.1.1") == False  # Five octets
    assert validate_ipv4_address("") == False  # Empty string
    assert validate_ipv4_address("1..1.1") == False  # Empty octet
    assert validate_ipv4_address("1.1.1.") == False  # Trailing dot

    assert validate_ipv4_address("192.168.1.a") == False  # Lowercase letters in octets
    assert validate_ipv4_address("192.168.1.A") == False  # Uppercase letters in octets
    assert validate_ipv4_address("192.168.1.+1") == False  # Positive sign in octets
    assert validate_ipv4_address("192.168.1.-1") == False  # Negative sign in octets
    assert validate_ipv4_address(" 192.168.1.1") == False  # Leading whitespace
    assert validate_ipv4_address("192.168.1.1 ") == False  # Trailing whitespace

def test_enforce_octet_values():
    assert validate_ipv4_address("256.0.0.0") == False  # First octet > 255
    assert validate_ipv4_address("1.256.1.1") == False  # Second octet > 255
    assert validate_ipv4_address("1.1.256.1") == False  # Third octet > 255
    assert validate_ipv4_address("0.0.0.256") == False  # Fourth octet > 255
    assert validate_ipv4_address("1.1.1.01") == False  # Leading zero in octet
    assert validate_ipv4_address("1.01.1.1") == False  # Leading zero in octet
    assert validate_ipv4_address("01.1.1.1") == False  # Leading zero in octet
    assert validate_ipv4_address("0.0.0.0") == False  # Specific case of network address

def test_require_host_assignable_final_octet():
    assert validate_ipv4_address("192.168.1.0") == False  # Final octet is 0 (network address)
    assert validate_ipv4_address("255.255.255.255") == False  # Final octet is 255 (broadcast address)
    assert validate_ipv4_address("192.168.1.254") == True  # Valid host address with final octet 254
    assert validate_ipv4_address("0.0.0.255") == False  # Final octet is 255 (broadcast address, but first three are 0)
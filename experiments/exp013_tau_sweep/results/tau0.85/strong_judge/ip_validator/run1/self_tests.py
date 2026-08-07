from solution import validate_ipv4_address

def test_accept_well_formed_host_addresses():
    assert validate_ipv4_address("1.1.1.1") == True  # Valid host address
    assert validate_ipv4_address("192.168.1.1") == True  # Valid host address
    assert validate_ipv4_address("10.0.0.1") == True  # Valid host address
    assert validate_ipv4_address("127.0.0.1") == True  # Valid host address
    assert validate_ipv4_address("255.0.1.1") == True  # Valid host address with first octet as 255
    assert validate_ipv4_address("1.255.0.1") == True  # Valid host address with second octet as 255
    assert validate_ipv4_address("0.1.255.1") == True  # Valid host address with first octet as 0

def test_reject_malformed_text():
    assert validate_ipv4_address("1.1.1") == False  # Only three octets
    assert validate_ipv4_address("1.1.1.1.1") == False  # Five octets
    assert validate_ipv4_address("") == False  # Empty string
    assert validate_ipv4_address("1..1.1") == False  # Empty octet
    assert validate_ipv4_address("1.1.1.") == False  # Trailing dot

    assert validate_ipv4_address("192.168.1.a") == False  # Invalid character (lowercase letter)
    assert validate_ipv4_address("192.168.1.A") == False  # Invalid character (uppercase letter)
    assert validate_ipv4_address("192.168.1.-1") == False  # Invalid character (negative sign)
    assert validate_ipv4_address("192.168.1.+1") == False  # Invalid character (plus sign)
    assert validate_ipv4_address(" 192.168.1.1") == False  # Leading whitespace
    assert validate_ipv4_address("192.168.1.1 ") == False  # Trailing whitespace

def test_enforce_octet_values():
    assert validate_ipv4_address("256.1.1.1") == False  # First octet out of range
    assert validate_ipv4_address("1.256.1.1") == False  # Second octet out of range
    assert validate_ipv4_address("1.1.256.1") == False  # Third octet out of range
    assert validate_ipv4_address("1.1.1.256") == False  # Fourth octet out of range

    assert validate_ipv4_address("01.1.1.1") == False  # Leading zero in first octet
    assert validate_ipv4_address("1.01.1.1") == False  # Leading zero in second octet
    assert validate_ipv4_address("1.1.01.1") == False  # Leading zero in third octet
    assert validate_ipv4_address("1.1.1.01") == False  # Leading zero in fourth octet
    assert validate_ipv4_address("0.1.1.1") == True  # Leading zero in first octet is allowed (0)

def test_require_host_assignable_final_octet():
    assert validate_ipv4_address("1.1.1.0") == False  # Final octet is 0 (network address)
    assert validate_ipv4_address("255.255.255.255") == False  # Final octet is 255 (broadcast address)
    assert validate_ipv4_address("192.168.1.255") == False  # Final octet is 255 (broadcast address)
    assert validate_ipv4_address("0.0.0.0") == False  # Explicitly testing all-zero address (network address)
    assert validate_ipv4_address("192.168.1.1") == True  # Final octet is within range (host assignable)
    assert validate_ipv4_address("192.168.1.254") == True  # Final octet is within range (host assignable)
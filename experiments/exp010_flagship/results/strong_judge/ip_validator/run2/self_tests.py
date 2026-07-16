from solution import validate_ipv4_address

def test_accept_well_formed_host_addresses():
    assert validate_ipv4_address("1.1.1.1")  # Valid address
    assert validate_ipv4_address("192.168.1.1")  # Valid address
    assert validate_ipv4_address("10.0.0.1")  # Valid address
    assert validate_ipv4_address("127.0.0.1")  # Valid address
    assert validate_ipv4_address("0.0.0.1")  # 0 in first position is valid
    assert validate_ipv4_address("255.255.255.1")  # 255 in first position is valid

def test_reject_malformed_text():
    assert not validate_ipv4_address("1.1.1")  # Three octets
    assert not validate_ipv4_address("1.1.1.1.1")  # Five octets
    assert not validate_ipv4_address("")  # Empty string
    assert not validate_ipv4_address("1..1.1")  # Empty octets
    assert not validate_ipv4_address(".1.1.1")  # Leading empty octet
    assert not validate_ipv4_address("1.1.1.")  # Trailing empty octet
    assert not validate_ipv4_address("1.1.1.a")  # Letter in octets
    assert not validate_ipv4_address("1.1.1.A")  # Uppercase letter in octets
    assert not validate_ipv4_address("1.1.1.1 ")  # Trailing whitespace
    assert not validate_ipv4_address(" 1.1.1.1")  # Leading whitespace
    assert not validate_ipv4_address("+1.1.1.1")  # Sign character
    assert not validate_ipv4_address("1.1.1.-1")  # Negative sign character

def test_enforce_octet_values():
    assert not validate_ipv4_address("256.1.1.1")  # Octet greater than 255
    assert not validate_ipv4_address("1.256.1.1")  # Octet greater than 255
    assert not validate_ipv4_address("1.1.256.1")  # Octet greater than 255
    assert not validate_ipv4_address("1.1.1.256")  # Octet greater than 255
    assert not validate_ipv4_address("01.1.1.1")  # Leading zero in first octet
    assert not validate_ipv4_address("1.01.1.1")  # Leading zero in second octet
    assert not validate_ipv4_address("1.1.01.1")  # Leading zero in third octet
    assert not validate_ipv4_address("1.1.1.01")  # Leading zero in final octet

def test_require_host_assignable_final_octet():
    assert not validate_ipv4_address("0.0.0.0")  # Final octet is 0 (network address)
    assert not validate_ipv4_address("1.1.1.0")  # Final octet is 0 (network address)
    assert not validate_ipv4_address("192.168.1.255")  # Final octet is 255 (broadcast address)
    assert not validate_ipv4_address("1.1.1.255")  # Final octet is 255 (broadcast address)
    assert validate_ipv4_address("192.168.1.254")  # Valid final octet
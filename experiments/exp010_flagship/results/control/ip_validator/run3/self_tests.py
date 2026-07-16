from solution import validate_ipv4_address

def test_accept_well_formed_host_addresses():
    # AC-1.1: Valid addresses
    assert validate_ipv4_address("1.1.1.1") == True  # Valid host address
    assert validate_ipv4_address("192.168.1.1") == True  # Valid host address
    assert validate_ipv4_address("10.0.0.1") == True  # Valid host address
    assert validate_ipv4_address("127.0.0.1") == True  # Valid host address

def test_reject_malformed_text():
    # AC-2.1: Invalid due to wrong number of octets
    assert validate_ipv4_address("1.1.1") == False  # Only three octets
    assert validate_ipv4_address("1.1.1.1.1") == False  # Five octets
    assert validate_ipv4_address("") == False  # Empty string
    assert validate_ipv4_address("1..1.1.1") == False  # Empty octet
    assert validate_ipv4_address("1.1.1.") == False  # Trailing empty octet

    # AC-2.2: Invalid due to non-digit characters
    assert validate_ipv4_address("1.1.1.a") == False  # Letter in octet
    assert validate_ipv4_address("1.1.1.-1") == False  # Negative sign in octet
    assert validate_ipv4_address(" 1.1.1.1") == False  # Leading whitespace
    assert validate_ipv4_address("1.1.1.1 ") == False  # Trailing whitespace

def test_enforce_octet_values():
    # AC-3.1: Invalid due to out of range octet
    assert validate_ipv4_address("256.0.0.1") == False  # Octet greater than 255
    assert validate_ipv4_address("1.2.3.256") == False  # Octet greater than 255
    assert validate_ipv4_address("1.2.300.4") == False  # Octet greater than 255

    # AC-3.2: Invalid due to leading zero
    assert validate_ipv4_address("01.1.1.1") == False  # Leading zero
    assert validate_ipv4_address("1.01.1.1") == False  # Leading zero
    assert validate_ipv4_address("1.1.01.1") == False  # Leading zero
    assert validate_ipv4_address("1.1.1.01") == False  # Leading zero

def test_require_host_assignable_final_octet():
    # AC-4.1: Invalid final octet as network address
    assert validate_ipv4_address("1.1.1.0") == False  # Final octet 0
    assert validate_ipv4_address("0.0.0.0") == False  # Network address

    # AC-4.2: Invalid final octet as broadcast address
    assert validate_ipv4_address("255.255.255.255") == False  # Final octet 255

    # AC-4.3: Valid final octet
    assert validate_ipv4_address("1.1.1.254") == True  # Valid host address
    assert validate_ipv4_address("0.0.0.1") == True  # Valid host address with 0 in first octet
    assert validate_ipv4_address("10.0.0.10") == True  # Valid host address
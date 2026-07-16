from solution import validate_ipv4_address

def test_accept_well_formed_host_addresses():
    # AC-1.1: Accept valid host addresses
    assert validate_ipv4_address("1.1.1.1") == True  # Valid host address
    assert validate_ipv4_address("192.168.1.1") == True  # Valid host address
    assert validate_ipv4_address("10.0.0.1") == True  # Valid host address
    assert validate_ipv4_address("127.0.0.1") == True  # Valid host address

def test_reject_malformed_text():
    # AC-2.1: Reject addresses not having exactly four octets
    assert validate_ipv4_address("1.1.1") == False  # Only three octets
    assert validate_ipv4_address("1.1.1.1.1") == False  # Five octets
    assert validate_ipv4_address("") == False  # Empty string
    assert validate_ipv4_address("1..1.1") == False  # Empty octet
    assert validate_ipv4_address(".1.1.1") == False  # Leading empty octet
    assert validate_ipv4_address("1.1.1.") == False  # Trailing empty octet

    # AC-2.2: Reject addresses with invalid characters
    assert validate_ipv4_address("192.168.a.1") == False  # Letters present
    assert validate_ipv4_address("192.168.1.-1") == False  # Negative sign
    assert validate_ipv4_address(" 192.168.1.1") == False  # Leading whitespace
    assert validate_ipv4_address("192.168.1.1 ") == False  # Trailing whitespace

def test_enforce_octet_values():
    # AC-3.1: Reject octets greater than 255
    assert validate_ipv4_address("256.0.0.1") == False  # First octet too high
    assert validate_ipv4_address("1.256.0.1") == False  # Second octet too high
    assert validate_ipv4_address("1.1.256.1") == False  # Third octet too high
    assert validate_ipv4_address("1.1.1.256") == False  # Final octet too high

    # AC-3.2: Reject octets with leading zeros
    assert validate_ipv4_address("01.1.1.1") == False  # Leading zero in first octet
    assert validate_ipv4_address("1.01.1.1") == False  # Leading zero in second octet
    assert validate_ipv4_address("1.1.01.1") == False  # Leading zero in third octet
    assert validate_ipv4_address("1.1.1.01") == False  # Leading zero in final octet

def test_require_host_assignable_final_octet():
    # AC-4.1: Reject addresses with final octet 0
    assert validate_ipv4_address("1.1.1.0") == False  # Final octet is 0
    assert validate_ipv4_address("0.0.0.0") == False  # Network address

    # AC-4.2: Reject addresses with final octet 255
    assert validate_ipv4_address("1.1.1.255") == False  # Final octet is 255
    assert validate_ipv4_address("255.255.255.255") == False  # Broadcast address

    # AC-4.3: Accept valid final octet values
    assert validate_ipv4_address("1.1.1.254") == True  # Valid final octet
    assert validate_ipv4_address("0.0.0.1") == True  # Valid host address with leading zeros in other parts
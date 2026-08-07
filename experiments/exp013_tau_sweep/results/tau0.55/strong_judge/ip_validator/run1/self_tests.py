from solution import validate_ipv4_address

def test_accept_well_formed_host_addresses():
    # AC-1.1: Valid addresses
    assert validate_ipv4_address("1.1.1.1") == True  # Valid host address
    assert validate_ipv4_address("192.168.1.1") == True  # Valid host address
    assert validate_ipv4_address("10.0.0.1") == True  # Valid host address
    assert validate_ipv4_address("127.0.0.1") == True  # Valid host address

def test_reject_malformed_text():
    # AC-2.1: Invalid due to the number of octets
    assert validate_ipv4_address("1.1.1") == False  # Only three octets
    assert validate_ipv4_address("1.1.1.1.1") == False  # Five octets
    assert validate_ipv4_address("") == False  # Empty string
    assert validate_ipv4_address("192.168..1") == False  # Empty octets due to double dot
    assert validate_ipv4_address("192.168.1.") == False  # Trailing dot
    assert validate_ipv4_address(".192.168.1") == False  # Leading dot resulting in empty octet

    # AC-2.2: Invalid due to non-digit characters
    assert validate_ipv4_address("192.168.1.a") == False  # Contains a letter
    assert validate_ipv4_address("192.168.1.A") == False  # Contains an uppercase letter
    assert validate_ipv4_address("192.168.1.+1") == False  # Contains a positive sign character
    assert validate_ipv4_address("192.168.1.-1") == False  # Contains a sign character
    assert validate_ipv4_address(" 192.168.1.1") == False  # Leading whitespace
    assert validate_ipv4_address("192.168.1.1 ") == False  # Trailing whitespace

def test_enforce_octet_values():
    # AC-3.1: Invalid due to octet values
    assert validate_ipv4_address("256.1.1.1") == False  # First octet > 255
    assert validate_ipv4_address("1.256.1.1") == False  # Second octet > 255
    assert validate_ipv4_address("1.1.256.1") == False  # Third octet > 255
    assert validate_ipv4_address("1.1.1.256") == False  # Fourth octet > 255

    # AC-3.2: Invalid due to leading zeros
    assert validate_ipv4_address("01.1.1.1") == False  # Leading zero in first octet
    assert validate_ipv4_address("1.01.1.1") == False  # Leading zero in second octet
    assert validate_ipv4_address("1.1.01.1") == False  # Leading zero in third octet
    assert validate_ipv4_address("1.1.1.01") == False  # Leading zero in fourth octet
    assert validate_ipv4_address("0.0.0.0") == False  # Leading zero in a valid case (but invalid address)

def test_require_host_assignable_final_octet():
    # AC-4.1: Invalid due to final octet being 0
    assert validate_ipv4_address("192.168.1.0") == False  # Final octet is network address

    # AC-4.2: Invalid due to final octet being 255
    assert validate_ipv4_address("255.255.255.255") == False  # Final octet is broadcast address

    # AC-4.3: Valid due to final octet being between 1 and 254
    assert validate_ipv4_address("192.168.1.1") == True  # Final octet is valid
    assert validate_ipv4_address("192.168.1.254") == True  # Final octet is valid
    assert validate_ipv4_address("0.0.0.1") == True  # Lone 0 in first position
    assert validate_ipv4_address("255.255.255.254") == True  # 255 in the first three positions
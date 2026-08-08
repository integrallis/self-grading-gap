# your complete test file
from solution import validate_ipv4_address

def test_accept_well_formed_host_addresses():
    # AC-1.1: Valid host addresses should be accepted
    assert validate_ipv4_address("1.1.1.1")  # Valid host address
    assert validate_ipv4_address("192.168.1.1")  # Valid host address
    assert validate_ipv4_address("10.0.0.1")  # Valid host address
    assert validate_ipv4_address("127.0.0.1")  # Valid host address

def test_reject_malformed_text():
    # AC-2.1: Text without exactly four octets should be rejected
    assert not validate_ipv4_address("1.1.1")  # Three octets
    assert not validate_ipv4_address("1.1.1.1.1")  # Five octets
    assert not validate_ipv4_address("")  # Empty string
    assert not validate_ipv4_address("1..1.1.1")  # Empty octet
    assert not validate_ipv4_address("1.1.1.")  # Trailing dot
    
    # AC-2.2: Non-digit characters should cause rejection
    assert not validate_ipv4_address("192.168.a.1")  # Letter in octet
    assert not validate_ipv4_address("192.168.1.1 ")  # Trailing whitespace
    assert not validate_ipv4_address(" 192.168.1.1")  # Leading whitespace
    assert not validate_ipv4_address("192.168.1.+1")  # Positive sign
    assert not validate_ipv4_address("192.168.A.1")  # Uppercase letter in octet
    assert not validate_ipv4_address("192.168.1.-1")  # Negative sign

def test_enforce_octet_values():
    # AC-3.1: An octet greater than 255 should be rejected
    assert not validate_ipv4_address("256.0.0.1")  # First octet too high
    assert not validate_ipv4_address("1.256.0.1")  # Second octet too high
    assert not validate_ipv4_address("1.1.256.1")  # Third octet too high
    assert not validate_ipv4_address("1.1.1.256")  # Fourth octet too high
    
    # AC-3.2: An octet with a leading zero should be rejected
    assert not validate_ipv4_address("01.1.1.1")  # Leading zero in first octet
    assert not validate_ipv4_address("1.01.1.1")  # Leading zero in second octet
    assert not validate_ipv4_address("1.1.01.1")  # Leading zero in third octet
    assert not validate_ipv4_address("1.1.1.01")  # Leading zero in fourth octet
    assert not validate_ipv4_address("0.0.0.0")  # Final octet is 0 (network address)
    assert validate_ipv4_address("0.1.1.1")  # Lone 0 is fine in non-final position
    assert validate_ipv4_address("255.255.255.1")  # 255 is fine in non-final position
    assert validate_ipv4_address("1.0.1.1")  # 0 is fine in second octet
    assert validate_ipv4_address("1.1.0.1")  # 0 is fine in third octet

def test_require_host_assignable_final_octet():
    # AC-4.1: Final octet of 0 should be rejected
    assert not validate_ipv4_address("1.1.1.0")  # Final octet is 0 (network address)
    assert not validate_ipv4_address("0.0.0.0")  # All octets are 0 (network address)
    
    # AC-4.2: Final octet of 255 should be rejected
    assert not validate_ipv4_address("255.255.255.255")  # All octets are 255 (broadcast address)
    
    # AC-4.3: Acceptable final octet values
    assert validate_ipv4_address("1.1.1.1")  # Valid final octet
    assert validate_ipv4_address("1.1.1.254")  # Largest acceptable final octet
    assert not validate_ipv4_address("1.1.1.255")  # Final octet is 255 (broadcast address)
import pytest
from solution import validate_ipv4_address

# US-1: Accept well-formed host addresses
def test_accept_valid_host_address_1():
    assert validate_ipv4_address("1.1.1.1") == True  # Valid address

def test_accept_valid_host_address_2():
    assert validate_ipv4_address("192.168.1.1") == True  # Valid address

def test_accept_valid_host_address_3():
    assert validate_ipv4_address("10.0.0.1") == True  # Valid address

def test_accept_valid_host_address_4():
    assert validate_ipv4_address("127.0.0.1") == True  # Valid address

# US-2: Reject malformed text
def test_reject_empty_string():
    assert validate_ipv4_address("") == False  # No octets

def test_reject_single_octet():
    assert validate_ipv4_address("1") == False  # Not enough octets

def test_reject_three_octets():
    assert validate_ipv4_address("1.1.1") == False  # Not enough octets

def test_reject_five_octets():
    assert validate_ipv4_address("1.1.1.1.1") == False  # Too many octets

def test_reject_doubled_dots():
    assert validate_ipv4_address("1..1.1.1") == False  # Empty octets

def test_reject_trailing_dots():
    assert validate_ipv4_address("1.1.1.") == False  # Empty octet at the end

def test_reject_letters():
    assert validate_ipv4_address("192.168.a.1") == False  # Contains letters

def test_reject_sign_characters():
    assert validate_ipv4_address("192.168.1.-1") == False  # Contains sign

def test_reject_leading_whitespace():
    assert validate_ipv4_address(" 192.168.1.1") == False  # Leading whitespace

# US-3: Enforce octet values
def test_reject_octet_greater_than_255():
    assert validate_ipv4_address("256.1.1.1") == False  # First octet too high

def test_reject_octet_with_leading_zero():
    assert validate_ipv4_address("01.1.1.1") == False  # Leading zero in first octet

def test_reject_octet_with_leading_zero_in_middle():
    assert validate_ipv4_address("1.01.1.1") == False  # Leading zero in second octet

def test_reject_octet_with_leading_zero_in_last():
    assert validate_ipv4_address("1.1.1.01") == False  # Leading zero in last octet

# US-4: Require a host-assignable final octet
def test_reject_final_octet_zero():
    assert validate_ipv4_address("192.168.1.0") == False  # Final octet is 0

def test_reject_final_octet_255():
    assert validate_ipv4_address("192.168.1.255") == False  # Final octet is 255

def test_accept_final_octet_254():
    assert validate_ipv4_address("192.168.1.254") == True  # Final octet is 254
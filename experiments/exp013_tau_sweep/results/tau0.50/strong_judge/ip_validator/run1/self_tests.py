# your complete test file
from solution import validate_ipv4_address

# User Stories
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
    assert validate_ipv4_address("") == False  # Empty string

def test_reject_three_octets():
    assert validate_ipv4_address("192.168.1") == False  # Only three octets

def test_reject_five_octets():
    assert validate_ipv4_address("192.168.1.1.1") == False  # Five octets

def test_reject_doubled_dots():
    assert validate_ipv4_address("192..168.1.1") == False  # Doubled dots

def test_reject_trailing_dots():
    assert validate_ipv4_address("192.168.1.") == False  # Trailing dot

def test_reject_leading_empty_octet():
    assert validate_ipv4_address(".192.168.1") == False  # Leading empty octet

def test_reject_non_digit_characters():
    assert validate_ipv4_address("192.168.a.1") == False  # Letter in octet

def test_reject_uppercase_letter_octet():
    assert validate_ipv4_address("192.168.A.1") == False  # Uppercase letter in octet

def test_reject_leading_whitespace():
    assert validate_ipv4_address(" 192.168.1.1") == False  # Leading whitespace

def test_reject_trailing_whitespace():
    assert validate_ipv4_address("192.168.1.1 ") == False  # Trailing whitespace

def test_reject_sign_character_negative():
    assert validate_ipv4_address("-1.1.1.1") == False  # Negative sign character

def test_reject_sign_character_positive():
    assert validate_ipv4_address("+1.1.1.1") == False  # Positive sign character

# US-3: Enforce octet values

def test_reject_octet_greater_than_255_position_1():
    assert validate_ipv4_address("256.168.1.1") == False  # Octet greater than 255

def test_reject_octet_greater_than_255_position_2():
    assert validate_ipv4_address("1.256.1.1") == False  # Octet greater than 255

def test_reject_octet_greater_than_255_position_3():
    assert validate_ipv4_address("1.1.256.1") == False  # Octet greater than 255

def test_reject_octet_greater_than_255_position_4():
    assert validate_ipv4_address("1.1.1.256") == False  # Octet greater than 255

def test_reject_octet_with_leading_zero_position_1():
    assert validate_ipv4_address("01.1.1.1") == False  # Leading zero in octet

def test_reject_octet_with_leading_zero_position_2():
    assert validate_ipv4_address("1.01.1.1") == False  # Leading zero in octet

def test_reject_octet_with_leading_zero_position_3():
    assert validate_ipv4_address("1.1.01.1") == False  # Leading zero in octet

def test_reject_octet_with_leading_zero_position_4():
    assert validate_ipv4_address("1.1.1.01") == False  # Leading zero in octet

# US-4: Require a host-assignable final octet

def test_reject_final_octet_zero():
    assert validate_ipv4_address("192.168.1.0") == False  # Final octet is 0

def test_reject_final_octet_255():
    assert validate_ipv4_address("192.168.1.255") == False  # Final octet is 255

def test_accept_final_octet_254():
    assert validate_ipv4_address("192.168.1.254") == True  # Final octet is 254

def test_accept_final_octet_1():
    assert validate_ipv4_address("192.168.1.1") == True  # Final octet is 1

def test_accept_intermediate_octet_zero():
    assert validate_ipv4_address("0.1.1.1") == True  # Intermediate octet is 0

def test_accept_intermediate_octet_255():
    assert validate_ipv4_address("255.255.255.1") == True  # Intermediate octet is 255

def test_reject_all_zero_network_address():
    assert validate_ipv4_address("0.0.0.0") == False  # All-zero network address

def test_reject_all_255_broadcast_address():
    assert validate_ipv4_address("255.255.255.255") == False  # All-255 broadcast address
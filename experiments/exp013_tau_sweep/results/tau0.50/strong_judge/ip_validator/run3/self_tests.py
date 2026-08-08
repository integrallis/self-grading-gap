# your complete test file
from solution import validate_ipv4_address

def test_accept_well_formed_host_addresses():
    # AC-1.1
    assert validate_ipv4_address("1.1.1.1") == True   # all octets valid, last octet 1
    assert validate_ipv4_address("192.168.1.1") == True  # all octets valid, last octet 1
    assert validate_ipv4_address("10.0.0.1") == True     # all octets valid, last octet 1
    assert validate_ipv4_address("127.0.0.1") == True    # all octets valid, last octet 1

def test_reject_malformed_text():
    # AC-2.1
    assert validate_ipv4_address("1.1.1") == False        # only 3 octets
    assert validate_ipv4_address("1.1.1.1.1") == False    # 5 octets
    assert validate_ipv4_address("") == False             # empty string
    assert validate_ipv4_address("1..1.1") == False       # empty octet due to double dot
    assert validate_ipv4_address("1.1.1.") == False       # trailing dot

    # AC-2.2
    assert validate_ipv4_address("192.168.1.a") == False  # contains letter
    assert validate_ipv4_address("192.168.1.1 ") == False  # trailing space
    assert validate_ipv4_address(" 192.168.1.1") == False  # leading space
    assert validate_ipv4_address("192.168.1.-1") == False  # sign character
    assert validate_ipv4_address("192.168.1.+1") == False  # positive sign
    assert validate_ipv4_address("192.168.1.A") == False    # uppercase letter

def test_enforce_octet_values():
    # AC-3.1
    assert validate_ipv4_address("256.1.1.1") == False     # first octet > 255
    assert validate_ipv4_address("1.256.1.1") == False     # second octet > 255
    assert validate_ipv4_address("1.1.256.1") == False     # third octet > 255
    assert validate_ipv4_address("1.1.1.256") == False     # last octet > 255

    # AC-3.2
    assert validate_ipv4_address("01.1.1.1") == False      # leading zero in first octet
    assert validate_ipv4_address("1.01.1.1") == False      # leading zero in second octet
    assert validate_ipv4_address("1.1.01.1") == False      # leading zero in third octet
    assert validate_ipv4_address("1.1.1.01") == False      # leading zero in last octet
    assert validate_ipv4_address("0.1.1.1") == True        # lone 0 in first octet is acceptable

def test_require_host_assignable_final_octet():
    # AC-4.1
    assert validate_ipv4_address("1.1.1.0") == False      # last octet is 0
    assert validate_ipv4_address("0.0.0.0") == False      # network address all zeros

    # AC-4.2
    assert validate_ipv4_address("1.1.1.255") == False    # last octet is 255
    assert validate_ipv4_address("255.255.255.255") == False  # broadcast address all 255s

    # AC-4.3
    assert validate_ipv4_address("1.1.1.254") == True     # last octet is 254 acceptable
    assert validate_ipv4_address("0.0.0.255") == False    # 255 in the last octet is not acceptable
    assert validate_ipv4_address("0.255.0.1") == True     # 255 in the first three octets is acceptable
    assert validate_ipv4_address("1.1.255.1") == True     # 255 in the second position is acceptable
    assert validate_ipv4_address("1.255.1.1") == True     # 255 in the third position is acceptable
    assert validate_ipv4_address("255.1.1.1") == True     # 255 in the first position is acceptable
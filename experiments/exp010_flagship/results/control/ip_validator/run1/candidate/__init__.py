def validate_ipv4_address(ip):
    # Split the IP address into octets
    octets = ip.split('.')
    # Check the number of octets
    if len(octets) != 4:
        return False
    # Check each octet
    for i, octet in enumerate(octets):
        # Check for empty octets
        if octet == '':
            return False
        # Check if the octet is a digit
        if not octet.isdigit():
            return False
        # Check for leading zeros
        if (octet.startswith('0') and len(octet) > 1) or (i == 0 and octet == '0'):
            return False
        # Convert octet to integer and check range
        num = int(octet)
        if num < 0 or num > 255:
            return False
    # Check the final octet for host-assignability
    final_octet = int(octets[-1])
    if final_octet == 0 or final_octet == 255:
        return False
    return True

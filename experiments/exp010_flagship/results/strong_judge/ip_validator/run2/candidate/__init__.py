def validate_ipv4_address(ip):
    # Split the address by dots
    octets = ip.split('.')
    # Check for exactly 4 octets
    if len(octets) != 4:
        return False
    for i, octet in enumerate(octets):
        # Check for empty octets
        if not octet:
            return False
        # Check if octet is a digit
        if not octet.isdigit():
            return False
        # Convert octet to integer
        value = int(octet)
        # Check for valid range and leading zeros
        if value < 0 or value > 255 or (len(octet) > 1 and octet[0] == '0'):
            return False
    # Check the final octet for host assignability
    if octets[-1] == '0' or octets[-1] == '255':
        return False
    return True

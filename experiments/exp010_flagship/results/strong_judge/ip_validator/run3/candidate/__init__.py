def validate_ipv4_address(ip):
    # Split the IP address into octets
    octets = ip.split('.')
    # Check for exactly 4 octets
    if len(octets) != 4:
        return False
    # Check each octet
    for i, octet in enumerate(octets):
        # Check if the octet is a digit
        if not octet.isdigit():
            return False
        # Check for leading zeros
        if len(octet) > 1 and octet[0] == '0':
            return False
        # Convert to integer and check range
        num = int(octet)
        if num < 0 or num > 255:
            return False
        # Check the final octet for host assignability
        if i == 3 and (num == 0 or num == 255):
            return False
    return True

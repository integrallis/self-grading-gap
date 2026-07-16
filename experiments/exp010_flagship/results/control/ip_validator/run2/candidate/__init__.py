def validate_ipv4_address(ip):
    # Split the IP address into octets
    octets = ip.split('.')
    # Check if there are exactly four octets
    if len(octets) != 4:
        return False
    for i, octet in enumerate(octets):
        # Check for invalid characters and leading whitespace
        if not octet.isdigit() or octet != str(int(octet)):
            return False
        # Check if the octet is in the valid range
        if int(octet) < 0 or int(octet) > 255:
            return False
        # Check for leading zeros
        if len(octet) > 1 and octet[0] == '0':
            return False
    # Check final octet restrictions
    final_octet = int(octets[-1])
    if final_octet == 0 or final_octet == 255:
        return False
    return True

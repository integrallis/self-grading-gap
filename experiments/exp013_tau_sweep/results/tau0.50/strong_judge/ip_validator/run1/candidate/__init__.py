def validate_ipv4_address(ip):
    # Split the input string by dots
    octets = ip.split('.');
    # Check for exactly four octets
    if len(octets) != 4:
        return False
    # Validate each octet
    for i, octet in enumerate(octets):
        # Check for leading/trailing whitespace
        if octet.strip() != octet:
            return False
        # Check if octet is a digit
        if not octet.isdigit():
            return False
        # Convert octet to int
        value = int(octet)
        # Check for valid range
        if value < 0 or value > 255:
            return False
        # Check for leading zeros
        if len(octet) > 1 and octet.startswith('0'):
            return False
        # Special case for the last octet
        if i == 3 and (value == 0 or value == 255):
            return False
    return True
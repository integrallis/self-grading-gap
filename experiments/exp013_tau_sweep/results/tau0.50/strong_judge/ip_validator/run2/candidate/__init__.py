def validate_ipv4_address(address: str) -> bool:
    # Split the address into octets
    octets = address.split('.')

    # Check for exactly four octets
    if len(octets) != 4:
        return False

    for i, octet in enumerate(octets):
        # Check if octet is a digit
        if not octet.isdigit():
            return False
        # Convert to integer
        num = int(octet)
        # Check for octet value and leading zeros
        if num < 0 or num > 255 or (octet != '0' and octet.startswith('0')):
            return False
        # Check for final octet conditions
        if i == 3:
            if num == 0 or num == 255:
                return False
    return True

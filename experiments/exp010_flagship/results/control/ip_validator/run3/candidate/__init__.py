def validate_ipv4_address(ip):
    # Split the IP address into octets
    octets = ip.split('.')

    # Must have exactly 4 octets
    if len(octets) != 4:
        return False

    for octet in octets:
        # Each octet must be a digit
        if not octet.isdigit():
            return False

        # Convert to integer
        num = int(octet)

        # Check for valid range (0-255)
        if num < 0 or num > 255:
            return False

        # Check for leading zeros
        if len(octet) > 1 and octet[0] == '0':
            return False

    # Check the final octet for host assignability
    last_octet = int(octets[-1])
    if last_octet == 0 or last_octet == 255:
        return False

    return True

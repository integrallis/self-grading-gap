def validate_ipv4_address(address):
    # Split the address into octets
    octets = address.split('.')
    # Check for the correct number of octets
    if len(octets) != 4:
        return False
    for octet in octets:
        # Check for non-digit characters
        if not octet.isdigit():
            return False
        # Convert the octet to an integer
        num = int(octet)
        # Check for valid range and leading zeros
        if num < 0 or num > 255 or (len(octet) > 1 and octet[0] == '0'):
            return False
    # Check if the final octet is valid for host assignment
    final_octet = int(octets[-1])
    if final_octet == 0 or final_octet == 255:
        return False
    return True
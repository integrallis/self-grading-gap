def validate_ipv4_address(address: str) -> bool:
    # Split the address into octets
    octets = address.split('.')
    # Check for valid number of octets
    if len(octets) != 4:
        return False
    # Validate each octet
    for i, octet in enumerate(octets):
        # Check for leading/trailing whitespace
        if octet.strip() != octet:
            return False
        # Check if it is a digit
        if not octet.isdigit():
            return False
        # Convert to integer
        num = int(octet)
        # Check ranges and leading zeros
        if not (0 <= num <= 255) or (octet != str(num)):
            return False
    # Final octet checks (not 0 or 255)
    final_octet = int(octets[-1])
    if final_octet == 0 or final_octet == 255:
        return False
    return True

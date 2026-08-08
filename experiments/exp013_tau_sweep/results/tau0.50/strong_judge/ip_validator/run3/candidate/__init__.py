def validate_ipv4_address(ip):
    # Split the input based on dots
    octets = ip.split('.')
    
    # Check for the correct number of octets
    if len(octets) != 4:
        return False
    
    for i, octet in enumerate(octets):
        # Check if the octet is a digit and convert to int
        if not octet.isdigit():
            return False
        num = int(octet)
        
        # Check for leading zeros and valid range
        if (octet != '0' and octet.startswith('0')) or num < 0 or num > 255:
            return False
        
        # Check if the last octet is host-assignable
        if i == 3 and (num == 0 or num == 255):
            return False
    
    return True

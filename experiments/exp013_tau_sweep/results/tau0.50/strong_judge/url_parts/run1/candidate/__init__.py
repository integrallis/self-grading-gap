import re

__version__ = "0.1.0"

def decompose_url(url):
    # Define the default ports for common protocols
    default_ports = {
        'http': 80,
        'https': 443,
        'ftp': 21,
        'sftp': 22
    }

    # Check for the protocol and split the URL
    match = re.match(r'^(?P<protocol>[a-zA-Z][a-zA-Z\d+.-]*):\/\/(?P<host>[^/?#]*)(?P<path>\/[^?#]*)?(\?(?P<query>[^#]*))?(#(?P<anchor>.*))?$', url)
    if not match:
        return f"Malformed URL, missing '://': '{url}'"

    protocol = match.group('protocol')
    host = match.group('host')
    path = match.group('path') or ''
    query = match.group('query') or ''
    anchor = match.group('anchor') or ''

    # Check for supported protocols
    if protocol not in default_ports:
        return f"Unsupported protocol: '{protocol}'"

    # Separate hostname and port text
    hostname, separator, port_part = host.partition(':')
    if separator:
        if not port_part.isdigit() or int(port_part) < 1 or int(port_part) > 65535:
            return f"Invalid port: '{port_part}'"
        port = int(port_part)
    else:
        port = default_ports[protocol]

    # Split hostname into subdomain and domain
    host_parts = hostname.split('.');
    if len(host_parts) == 0:
        return "Missing host"
    if hostname == "localhost":
        domain = "localhost"
        subdomain = ""
    elif len(host_parts) < 2:
        return "Missing host"
    else:
        domain = '.'.join(host_parts[-2:])
        subdomain = '.'.join(host_parts[:-2]) if len(host_parts) > 2 else ''

    # Check for valid top-level domains
    recognized_tlds = {"com", "net", "org", "int", "edu", "gov", "mil"}
    tld = host_parts[-1]
    if hostname != "localhost" and tld not in recognized_tlds:
        return f"Unsupported top-level domain: '{tld}'"

    return {
        'protocol': protocol,
        'subdomain': subdomain,
        'domain': domain,
        'port': port,
        'path': path.lstrip('/'),  # Remove leading slash
        'query': query,
        'anchor': anchor
    }
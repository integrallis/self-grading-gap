import re

__version__ = "0.1.0"

def decompose_url(url):
    # Check and parse the URL using regex
    match = re.match(r'^(?P<protocol>\w+)://(?P<subdomain>[^./]+\.)?(?P<domain>[^./]+\.[a-z]{2,})(?::(?P<port>\d+))?(/(?P<path>[^?#]*))?(\?(?P<query>[^#]*))?(#(?P<anchor>.*))?$', url)
    if not match:
        raise ValueError(f"Malformed URL, missing '://': '{url}'")

    # Extract components from the match
    protocol = match.group('protocol')
    subdomain = match.group('subdomain') or ""
    domain = match.group('domain')
    port = match.group('port')
    path = match.group('path') or ""
    query = match.group('query') or ""
    anchor = match.group('anchor') or ""

    # Validate protocol
    if protocol not in ['http', 'https', 'ftp', 'sftp']:
        raise ValueError(f"Unsupported protocol: '{protocol}'")

    # Validate top-level domain
    if not re.match(r'[a-z]{2,}', domain.split('.')[-1]):
        raise ValueError(f"Unsupported top-level domain: '{domain.split('.')[-1]}'")

    # Set default port
    if port:
        try:
            port = int(port)
        except ValueError:
            raise ValueError(f"Invalid port: '{port}'")
    else:
        port = 80 if protocol == 'http' else 443 if protocol == 'https' else 21 if protocol == 'ftp' else 22 if protocol == 'sftp' else None

    if port is None:
        raise ValueError(f"Unsupported protocol: '{protocol}'")

    # Return the decomposed URL
    return {
        'protocol': protocol,
        'subdomain': subdomain.rstrip('.'),
        'domain': domain,
        'port': port,
        'path': path,
        'query': query,
        'anchor': anchor
    }
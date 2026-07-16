def decompose_url(url):
    import re
    import pytest

    # Protocols and their default ports
    protocols = {
        'http': 80,
        'https': 443,
        'ftp': 21,
        'sftp': 22
    }

    # Regular expression to match the URL structure
    regex = re.compile(r'^(?P<protocol>\w+)://(?P<host>[^:/]+)(?::(?P<port>\d+))?(?P<path>/[^?#]*)?(?:\?(?P<query>[^#]*))?(#(?P<anchor>.*))?$')
    match = regex.match(url)

    if not match:
        raise ValueError(f"Malformed URL, missing '://': '{url}'")

    protocol = match.group('protocol')
    host = match.group('host')
    port = match.group('port')
    path = match.group('path') or ''
    query = match.group('query') or ''
    anchor = match.group('anchor') or ''

    if protocol not in protocols:
        raise ValueError(f"Unsupported protocol: '{protocol}'")

    if not host:
        raise ValueError("Missing host")

    # Validate the top-level domain (TLD)
    tld = host.split('.')[-1]
    if not re.match(r'^[a-z]{2,}$', tld):
        raise ValueError(f"Unsupported top-level domain: '{tld}'")

    if port:
        if not port.isdigit() or int(port) < 1 or int(port) > 65535:
            raise ValueError(f"Invalid port: '{port}'")
        port = int(port)
    else:
        port = protocols[protocol]

    # Split host into subdomain and domain
    domain_parts = host.split('.')
    domain = '.'.join(domain_parts[-2:])
    subdomain = '.'.join(domain_parts[:-2])

    return {
        'protocol': protocol,
        'subdomain': subdomain,
        'domain': domain,
        'port': port,
        'path': path,
        'query': query,
        'anchor': anchor
    }
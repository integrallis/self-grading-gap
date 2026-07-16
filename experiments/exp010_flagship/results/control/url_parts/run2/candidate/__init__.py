import pytest

recognized_tlds = ['com', 'org', 'net', 'edu', 'gov', 'mil', 'info', 'io', 'co']

def decompose_url(url):
    # Validate the URL format
    if '://' not in url:
        raise ValueError(f"Malformed URL, missing '://': '{url}'")

    protocol, rest = url.split('://', 1)
    if protocol not in ['http', 'https', 'ftp', 'sftp']:
        raise ValueError(f"Unsupported protocol: '{protocol}'")

    # Split host and path
    host_path = rest.split('/', 1)
    host_port = host_path[0]
    path = host_path[1] if len(host_path) > 1 else ''

    # Handle query and anchor
    query = ''
    anchor = ''
    if '?' in path:
        path, query = path.split('?', 1)
    if '#' in path:
        path, anchor = path.split('#', 1)

    # Split host and port
    if ':' in host_port:
        host, port = host_port.split(':', 1)
        if not port.isdigit():
            raise ValueError(f"Invalid port: '{port}'")
        port = int(port)
    else:
        host = host_port
        port = 80 if protocol == 'http' else 443 if protocol == 'https' else 21 if protocol == 'ftp' else 22

    # Check for empty host
    if not host:
        raise ValueError("Missing host")

    # Check top-level domain
    domain_parts = host.split('.')
    if len(domain_parts) < 2 or domain_parts[-1] not in recognized_tlds:
        raise ValueError(f"Unsupported top-level domain: '{domain_parts[-1]}'")

    # Handle subdomain and domain
    if len(domain_parts) > 2:
        subdomain = '.'.join(domain_parts[:-2])
        domain = '.'.join(domain_parts[-2:])
    else:
        subdomain = ''
        domain = host

    return {
        'protocol': protocol,
        'subdomain': subdomain,
        'domain': domain,
        'port': port,
        'path': path,
        'query': query,
        'anchor': anchor
    }
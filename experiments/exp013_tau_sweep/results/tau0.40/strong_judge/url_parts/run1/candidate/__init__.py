def decompose_url(url):
    # Check for protocol
    if '://' not in url:
        raise Exception(f"Malformed URL, missing '://': '{url}'")
    protocol, rest = url.split('://', 1)

    # Validate protocol
    valid_protocols = {'http': 80, 'https': 443, 'ftp': 21, 'sftp': 22}
    if protocol not in valid_protocols:
        raise Exception(f"Unsupported protocol: '{protocol}'")

    # Handle query and anchor first
    before_fragment, hash_sep, anchor = rest.partition('#')
    if hash_sep == '':
        anchor = ''
    before_query, query_sep, query = before_fragment.partition('?')
    if query_sep == '':
        query = ''
    host, slash_sep, path = before_query.partition('/')
    if slash_sep == '':
        path = ''

    # Handle port
    if ':' in host:
        host, port = host.split(':', 1)
        if not port.isdigit() or not (0 <= int(port) <= 65535):
            raise Exception(f"Invalid port: '{port}'")
        port = int(port)
    else:
        port = valid_protocols[protocol]

    if host == '':
        raise Exception("Missing host")

    # Special case for localhost
    if host == 'localhost':
        domain = 'localhost'
        subdomain = ''
    else:
        domain_parts = host.split('.');
        if len(domain_parts) < 2:
            raise Exception("Missing domain")
        domain = '.'.join(domain_parts[-2:])  # Last two parts are considered the domain
        subdomain = '.'.join(domain_parts[:-2]) if len(domain_parts) > 2 else ''

        # Validate TLD
        supported_tlds = ['com', 'net', 'org', 'int', 'edu', 'gov', 'mil']
        tld = domain.split('.')[-1]
        if tld not in supported_tlds:
            raise Exception(f"Unsupported top-level domain: '{tld}'")

    return {
        'protocol': protocol,
        'subdomain': subdomain,
        'domain': domain,
        'port': port,
        'path': path,
        'query': query,
        'anchor': anchor
    }
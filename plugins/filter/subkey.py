#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.errors import AnsibleFilterError
from ansible.module_utils._text import to_text
import subprocess
import json

DOCUMENTATION = '''
name: subkey_inspect
author: Parity Technologies
version_added: "1.10.8"
short_description: Inspects crypto keys using the Subkey utility
description:
    - Filter that runs the Subkey inspect command to analyze cryptographic keys
    - Supports various networks and schemes
    - Can output public key information
    - Returns JSON formatted data about the key
options:
    uri:
        description: The URI or key to inspect
        type: str
        required: true
    network:
        description: The network to use for the inspection
        type: str
        required: false
        default: ''
    scheme:
        description: The cryptographic scheme to use
        type: str
        required: false
        default: ''
    public:
        description: Whether to only show public key information
        type: bool
        required: false
        default: false
'''

EXAMPLES = '''
# Basic key inspection
- debug:
    msg: "{{ 'key_uri' | subkey_inspect }}"

# Inspect with specific network
- debug:
    msg: "{{ 'key_uri' | subkey_inspect(network='kusama') }}"

# Inspect with specific scheme and show only public info
- debug:
    msg: "{{ 'key_uri' | subkey_inspect(scheme='sr25519', public=true) }}"
'''

RETURN = '''
ss58:
    description: The SS58 address of the key
    type: str
    sample: "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"
public_key:
    description: The public key in hex format
    type: str
    sample: "0xd43593c715fdd31c61141abd04a99fd6822c8558854ccde39a5684e7a56da27d"
account_id:
    description: The account ID
    type: str
    sample: "d43593c715fdd31c61141abd04a99fd6822c8558854ccde39a5684e7a56da27d"
'''


def subkey_inspect(uri, network='', scheme='', public=False):
    """Run subkey inspect command and return output."""
    uri = to_text(uri, errors='surrogate_or_strict', nonstring='simplerepr')

    args = []
    log_uri = '<URI>'
    if scheme:
        args.extend(['--scheme', scheme])
    if network:
        args.extend(['--network', network])
    if public:
        args.extend(['--public'])
        log_uri = uri

    try:
        process = subprocess.Popen(['subkey', 'inspect', uri, "--output-type=json", *args],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   universal_newlines=True)
    except FileNotFoundError:
        raise AnsibleFilterError(
            "subkey binary is required for this filter. Please, install it on local machine: sudo curl -fSL -o "
            "/usr/local/bin/subkey 'https://releases.parity.io/substrate/x86_64-debian%3Astretch/v3.0.0/subkey/subkey' "
            "&& chmod +x /usr/local/bin/subkey"
        )
    except Exception as e:
        raise AnsibleFilterError(
            'Error running subkey command. \nCommand: subkey inspect %s %s \nError: %s'
            % (log_uri, ' '.join(args), e))
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        raise AnsibleFilterError('Error running subkey command. \nCommand: subkey inspect %s %s \nstdout: %s \nstderr: %s'
                                 % (log_uri, ' '.join(args), stdout, stderr))
    try:
        output = json.loads(stdout)
    except Exception as e:
        raise AnsibleFilterError('Error parsing json:\n%s \nError: %s' % (stdout, e))

    return output


class FilterModule(object):
    """ Subkey filter """

    def filters(self):
        return {
            'subkey_inspect': subkey_inspect
        }

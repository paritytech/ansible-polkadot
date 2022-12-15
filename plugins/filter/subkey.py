#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.errors import AnsibleFilterError
from ansible.module_utils._text import to_text
import subprocess
import json


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



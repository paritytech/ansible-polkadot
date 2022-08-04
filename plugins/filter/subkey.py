#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.errors import AnsibleFilterError
from ansible.module_utils._text import to_text
import subprocess
import json


def subkey_inspect(a, network='', scheme='', public=False):
    """Run subkey inspect command and return output."""
    a = to_text(a, errors='surrogate_or_strict', nonstring='simplerepr')

    args = []
    if scheme:
        args.extend(['--scheme', scheme])
    if network:
        args.extend(['--network', network])
    if public:
        args.extend(['--public'])

    try:
        process = subprocess.Popen(['subkey', 'inspect', a, "--output-type=json", *args],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   universal_newlines=True)
    except Exception as e:
        raise AnsibleFilterError(
            'Error running subkey command. \nCommand: subkey inspect %s %s \nError: %s'
            % (a, ' '.join(args), e))
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        raise AnsibleFilterError('Error running subkey command. \nCommand: subkey inspect %s %s \nstdout: %s \nstderr: %s'
                                 % (a, ' '.join(args), stdout, stderr))
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



#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import json
import subprocess
import re


def main():
    print(json.dumps(inventory(), sort_keys=True, indent=2))


def inventory():
    ip_list = list(find_ip())

    return {
        'all': {
            'hosts': [ip_list],
            'vars': {
                'ansible_connection': 'local'
            },
        },
        '_meta': {
            'hostvars': {
                ip_list[0]: {
                    'ansible_ssh_user': 'ansible'
                },
                ip_list[1]: {
                    'ansible_ssh_user': 'ansible'
                }
            },
        },
        'ip': [ip_list]
    }


def find_ip():
    lines = subprocess.check_output(['arp', '-a']).decode('utf-8').split('\n')
    lines = filter(None, lines)  # fastest
    for line in lines:
        # if re.search('0:4a:77:e2:55:f', line):
        ip = re.search(r"(\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b)", line)
        yield ip.group()


if __name__ == '__main__':
    main()

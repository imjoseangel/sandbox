#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Terraform Wrapper
"""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import argparse
import logging
import os
import shutil
import subprocess
import sys
import pandas as pd


class ParseArgs():
    """ Parse command line arguments """

    def __init__(self) -> None:

        # Parse arguments passed at cli
        self.parse_arguments()

    def parse_arguments(self):
        """ Parse arguments passed at cli """

        description = '''
    This script is used to launch multiple Terraform executions.'''

        parser = argparse.ArgumentParser(
            description=description, formatter_class=argparse.RawTextHelpFormatter)

        parser.add_argument('-s', '--statename',
                            help='Terraform state name. Defaults to terraform.tfstate',
                            required=False,
                            default='terraform.tfstate')

        parser.add_argument('-c', '--csvfile',
                            help='CSV file with the list of Terraform executions. Defaults to terraform.csv',
                            required=False,
                            default='terraform.csv')

        self.args = parser.parse_args()


def runterraform(verb, args=''):
    """ Run Terraform """
    validverbs = {'init', 'apply', 'destroy'}

    if verb not in validverbs:
        raise ValueError(f'Verb must be one of {validverbs}')

    try:

        tf_proc = subprocess.Popen('terraform ' + verb + ' ' + args,
                                   shell=True,
                                   executable="/bin/bash",
                                   stdin=None,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)

        for line in tf_proc.stdout:
            logging.info(line.strip().decode('utf-8'))

        tf_proc.stdout.close()
        tf_proc.wait()

        return tf_proc

    except subprocess.CalledProcessError as exception:
        print(exception.output)
        sys.exit(1)


def main():
    """ Main function """

    options = ParseArgs()

    logging.basicConfig(format="%(asctime)s - %(message)s",
                        datefmt="%d-%b-%y %H:%M:%S", stream=sys.stdout, level=logging.INFO)

    appservices = pd.read_csv(options.args.csvfile, sep=',')

    for item in appservices.iterrows():

        tfdir = ".terraform"
        appname = item[1]['NAME']
        resourcegroup = item[1]['RESOURCE GROUP']

        if os.path.exists(tfdir):
            try:
                shutil.rmtree(tfdir)
            except OSError as oserror_exception:
                logging.error(oserror_exception.filename,
                              oserror_exception.strerror)

        if os.path.exists('.terraform.lock.hcl'):
            try:
                os.remove('.terraform.lock.hcl')
            except OSError as oserror_exception:
                logging.error(oserror_exception.filename,
                              oserror_exception.strerror)

        runterraform(
            'init', f'-upgrade -backend-config=key={appname}-{options.args.statename}')

        runterraform(
            'apply', f'-auto-approve -var="name={appname}" -var="resource_group={resourcegroup}"')


if __name__ == '__main__':
    main()

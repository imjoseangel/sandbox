#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import logging
import os
import shutil
import subprocess
import sys
import pandas as pd


def runterraform(verb, args=''):
    """ Run Terraform """
    validverbs = {'init', 'apply', 'destroy'}

    if verb not in validverbs:
        raise ValueError('Verb must be one of {0}'.format(validverbs))

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

    logging.basicConfig(format="%(asctime)s - %(message)s",
                        datefmt="%d-%b-%y %H:%M:%S", stream=sys.stdout, level=logging.INFO)

    appservices = pd.read_csv('appservices.csv', sep=',')

    for item in appservices.iterrows():

        tfdir = ".terraform"
        appname = item[1]['NAME']
        resourcegroup = item[1]['RESOURCE GROUP']

        if os.path.exists(tfdir):
            try:
                shutil.rmtree(tfdir)
            except OSError as e:
                logging.error(e.filename, e.strerror)

        if os.path.exists('.terraform.lock.hcl'):
            try:
                os.remove('.terraform.lock.hcl')
            except OSError as e:
                logging.error(e.filename, e.strerror)

        runterraform(
            'init', '-upgrade -backend-config=key={0}-customdns.tfstate'
            .format(appname))

        runterraform(
            'apply', '-auto-approve -var="name={0}" -var="resource_group={1}"'
            .format(appname, resourcegroup))


if __name__ == '__main__':
    main()

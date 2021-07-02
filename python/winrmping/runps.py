#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import logging
import os
import sched
import time
import winrm

path = os.path.dirname(os.path.realpath(__file__))
# logging.basicConfig(format="%(asctime)s - %(message)s",
#                     datefmt="%d-%b-%y %H:%M:%S", stream=sys.stderr, level=logging.INFO)

logging.basicConfig(filename=f"{path}/access.log", filemode="a", format="%(asctime)s - %(message)s",
                    datefmt="%d-%b-%y %H:%M:%S", level=logging.INFO)

sched = sched.scheduler(time.time, time.sleep)

bastion = os.environ['HOST']
user = os.environ['USER']
domain = os.environ['DOMAIN']
password = os.environ['PASS']
thost = os.environ['THOST']
tdomain = os.environ['TDOMAIN']
tport = os.environ['TPORT']

serverlist = ["SERVER1", "SERVER2"]

session = winrm.Session(bastion, auth=(
    '{}@{}'.format(user, domain), password), transport='ntlm')


def sqlping(scheduler):

    for server in serverlist:
        # https://stackoverflow.com/questions/40029235/save-pscredential-in-the-file
        result = session.run_ps(f"$cred = Import-CliXml -Path 'cred.xml'; Invoke-command "
                                f"-ComputerName {server}.{tdomain} -ScriptBlock {{(Test-NetConnection "
                                f"-ComputerName {thost}.{tdomain} -Port {tport}).TcpTestSucceeded}}"
                                f"-Credential $cred")
        logging.info(server)
        logging.info((result.std_out).decode("utf-8"))

    # do your stuff
    sched.enter(1, 1, sqlping, (scheduler,))


def main():

    sched.enter(1, 1, sqlping, (sched,))
    sched.run()


if __name__ == '__main__':
    main()

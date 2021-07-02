#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import winrm
import logging
import os
import sys
import json
import sched
import socket
import time

path = os.path.dirname(os.path.realpath(__file__))
# logging.basicConfig(format="%(asctime)s - %(message)s",
#                     datefmt="%d-%b-%y %H:%M:%S", stream=sys.stderr, level=logging.INFO)

logging.basicConfig(filename=f"{path}/access.log", filemode="a", format="%(asctime)s - %(message)s",
                    datefmt="%d-%b-%y %H:%M:%S", level=logging.INFO)

sched = sched.scheduler(time.time, time.sleep)

host = "bastion"
domain = "imjoseangel.local"
user = os.environ['USER']
password = os.environ['PASS']

serverlist = ["SERVER1", "SERVER2"]

session = winrm.Session(host, auth=(
    '{}@{}'.format(user, domain), password), transport='ntlm')


def sqlping(scheduler):

    for server in serverlist:
        # https://stackoverflow.com/questions/40029235/save-pscredential-in-the-file
        result = session.run_ps(
            f"$cred = Import-CliXml -Path 'cred.xml'; Invoke-command -ComputerName {server}.{domain} -ScriptBlock {{(Test-NetConnection -ComputerName PingServer.{domain} -Port 49508).TcpTestSucceeded}} -Credential $cred")
        logging.info(server)
        logging.info((result.std_out).decode("utf-8"))

    # do your stuff
    sched.enter(1, 1, sqlping, (scheduler,))


def main():

    sched.enter(1, 1, sqlping, (sched,))
    sched.run()


if __name__ == '__main__':
    main()

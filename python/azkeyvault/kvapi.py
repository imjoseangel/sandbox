#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python Template
"""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from dataclasses import dataclass
import logging
import os
import sys
import time
from waitress import serve
from flask import Flask, request

from azure.keyvault.secrets import SecretClient
from azure.identity import ClientSecretCredential

logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s",
    level=logging.INFO,
    datefmt="%d-%b-%y %H:%M:%S",
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

clientid = os.getenv('AZURE_CLIENT_ID')
clientsecret = os.getenv('AZURE_CLIENT_SECRET')
tenantid = os.getenv('AZURE_TENANT_ID')
secretName = os.getenv('AZURE_SECRET_NAME')
keyVaultName = os.getenv('AZURE_KEY_VAULT_NAME')


@ dataclass
class RunJob:

    @ staticmethod
    def animation():
        anime = "|/-\\"
        for i in range(10):
            time.sleep(0.1)
            sys.stdout.write("\r" + anime[i % len(anime)])
            sys.stdout.flush()

    @ staticmethod
    def get_running():

        try:

            KVUri = f"https://{keyVaultName}.vault.azure.net"

            credential = ClientSecretCredential(client_id=clientid,
                                                client_secret=clientsecret,
                                                tenant_id=tenantid)

            client = SecretClient(vault_url=KVUri, credential=credential)

            retrieved_secret = client.get_secret(secretName)

            # Output is apple for [120, 1]
            logger.info(retrieved_secret.value)
            return f"{retrieved_secret.value}"

        except KeyError as e:
            logger.error(e)
            return f"Error: Incorrect {e}"

        except TypeError as e:
            logger.error(e)
            return f"Error: Incorrect {e}"


app = Flask(__name__)
jobrequests = RunJob()


@ app.route('/', methods=['GET'])
def home():
    if request.method == 'GET':
        logger.info("Running Keyvault")
        return jobrequests.get_running()
    else:
        return 'healthy'


def main():
    """
    Main function
    """
    os.system('clear')

    logging.info("""
██╗  ██╗ █████╗ ███████╗████████╗███████╗███████╗████████╗
██║ ██╔╝██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝
█████╔╝ ╚█████╔╝███████╗   ██║   █████╗  ███████╗   ██║
██╔═██╗ ██╔══██╗╚════██║   ██║   ██╔══╝  ╚════██║   ██║
██║  ██╗╚█████╔╝███████║   ██║   ███████╗███████║   ██║
╚═╝  ╚═╝ ╚════╝ ╚══════╝   ╚═╝   ╚══════╝╚══════╝   ╚═╝
                                                            """)
    try:
        serve(app, port="8080", threads=25, host="127.0.0.1")
    except OSError as e:
        logging.error(e)


if __name__ == '__main__':
    main()

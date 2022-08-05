import os
import time
import sys
import fnmatch
import requests
import subprocess
import logging
import urllib.request
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool as ThreadPool

logging.basicConfig(format="%(asctime)s - %(message)s",
                    datefmt="%d-%b-%y %H:%M:%S", stream=sys.stdout,
                    level=logging.INFO)

pip_proc = subprocess.Popen('pipreqs . --force',
                            shell=True,
                            executable="/bin/bash",
                            stdin=None,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)

for line in pip_proc.stdout:
    logging.info(line.strip().decode('utf-8'))

pip_proc.stdout.close()
pip_proc.wait()

print(pip_proc)

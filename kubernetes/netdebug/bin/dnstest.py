#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python Template
"""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)
import asyncio
import concurrent.futures
import logging
import sys
import requests

logging.basicConfig(format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
                    datefmt="%d-%b-%y %H:%M:%S", stream=sys.stdout, level=logging.INFO)

logger = logging.getLogger('httprequests')
logging.getLogger("chardet.charsetprober").disabled = True


async def main():

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:

        fetch = asyncio.get_event_loop()
        futures = [
            fetch.run_in_executor(
                executor,
                requests.get,
                'http://www.example.com'
            )
            for i in range(20)
        ]
        for request in await asyncio.gather(*futures):
            logger.info(request)


while True:

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


if __name__ == '__main__':
    main()

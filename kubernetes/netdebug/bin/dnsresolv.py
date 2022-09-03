import logging
import os
import sys
import asyncio
import aiodns


logging.basicConfig(format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
                    datefmt="%d-%b-%y %H:%M:%S", stream=sys.stdout, level=logging.INFO)

logger = logging.getLogger('dnsresolv')
logging.getLogger("chardet.charsetprober").disabled = True

benchuri = os.environ.get('BENCHURI', 'www.example.com')

loop = asyncio.get_event_loop()
resolver = aiodns.DNSResolver(loop=loop)


async def query(name, query_type):
    return await resolver.query(name, query_type)


while True:
    coro = query(benchuri, 'A')
    result = loop.run_until_complete(coro)

    logger.info(result)

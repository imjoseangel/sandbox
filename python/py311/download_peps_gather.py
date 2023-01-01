# download_peps_gather.py

import asyncio
import aiohttp

PEP_URL = (
    "https://raw.githubusercontent.com/python/peps/master/pep-{pep:04d}.txt"
)


async def download_pep(session, pep):
    print(f"Downloading PEP {pep}")
    url = PEP_URL.format(pep=pep)
    async with session.get(url, params={}) as response:
        pep_text = await response.text()

    title = pep_text.split("\n")[1].removeprefix("Title:").strip()
    print(f"Downloaded PEP {pep}: {title}")


async def download_peps(session, peps):
    tasks = [asyncio.create_task(download_pep(session, pep)) for pep in peps]
    await asyncio.gather(*tasks)


async def main(peps):
    async with aiohttp.ClientSession() as session:
        await download_peps(session, peps)


asyncio.run(main([492, 525, 530, 3148, 3156]))

import asyncio
import aiohttp

from .truck import Cargo, Source, Destination

class HttpSource(Source):

    def __init__(self, url: str):
        self._url = url

    async def load(self, cargo: Cargo):
        async with aiohttp.ClientSession() as session:
            async with session.get(self._url) as response:
                with cargo.fill() as f:
                    while True:
                        chunk = await response.content.read(1024*1024*5)
                        if not chunk:
                            break
                        f.write(chunk)

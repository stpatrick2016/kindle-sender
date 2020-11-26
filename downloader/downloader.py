from abc import ABC, abstractmethod
import asyncio
import aiohttp
import boto3
from arnparse import arnparse
import os
import tempfile

class Downloader(ABC):

    @abstractmethod
    async def download(self, url: str, filename: str):
        pass

    @staticmethod
    def factory(target: str):
        if target.startswith("arn:aws:s3"):
            return S3Downloader(target) 
        else: 
            raise Exception(f"Unsupported target type: {target}")

class S3Downloader(Downloader):
    def __init__(self, target: str):
        self._target = target

    async def download(self, url: str, filename: str):
        tempdir = tempfile.gettempdir()
        fpath = f"{tempdir}/{filename}.mobi"
        print(f"Temporary file is {fpath}")
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                with open(fpath, "wb") as f:
                    while True:
                        chunk = await response.content.read(1024*1024*5)
                        if not chunk:
                            break
                        f.write(chunk)
        arn = arnparse(self._target)
        s3 = boto3.client("s3")
        s3.upload_file(fpath, arn.resource, f"{filename}.mobi")
        os.remove(fpath)
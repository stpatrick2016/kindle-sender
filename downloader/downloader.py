from abc import ABC, abstractmethod
import asyncio
import aiohttp
import boto3
from arnparse import arnparse

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
        arn = arnparse(self._target)
        s3 = boto3.client("s3")
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                s3.upload_fileobj(response, arn.resource, filename)
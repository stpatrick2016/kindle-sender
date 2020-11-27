import boto3

from .truck import Cargo, Source, Destination

class S3Destination(Destination):
    
    def __init__(self, bucket:str, key: str):
        self._bucket = bucket
        self._key = key

    async def unload(self, cargo: Cargo):
        s3 = boto3.client("s3")
        with cargo.empty() as f:
            s3.upload_fileobj(f, self._bucket, self._key)

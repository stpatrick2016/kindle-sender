from arnparse import arnparse

from .truck import Cargo, Source, Destination, Truck, GroundedCargo
from .s3_store import S3Destination
from .http_store import HttpSource

class Depot:
    def __init__(self, cargo: Cargo, source: Source, destination: Destination):
        self._cargo = cargo
        self._source = source
        self._dest = destination

    async def dispatch(self):
        truck = Truck(self._source, self._dest)
        await truck.deliver(self._cargo)

    @classmethod
    def from_http_to_s3(cls, url: str, bucket: str, filename: str):
        cargo = GroundedCargo()
        source = HttpSource(url)
        if bucket.startswith("arn:aws:s3"):
            bucket = arnparse(bucket).resource
        dest = S3Destination(bucket, filename)
        return cls(cargo, source, dest)
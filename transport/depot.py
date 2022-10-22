from arnparse import arnparse

from .http_store import HttpSource
from .s3_store import S3Destination, S3Source
from .smtp_store import SmtpDestination
from .truck import Cargo, Source, Destination, Truck, GroundedCargo


class Depot:
    def __init__(self, cargo: Cargo, source: Source, destination: Destination):
        self._cargo = cargo
        self._source = source
        self._dest = destination

    async def dispatch(self):
        print("Dispatching truck...")
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

    @classmethod
    def from_s3_to_mail(cls, bucket: str, filename: str, address: str, server: str, port: int, user: str, password: str):
        if bucket.startswith("arn:aws:s3"):
            bucket = arnparse(bucket).resource
        cargo = GroundedCargo()
        source = S3Source(bucket, filename)
        dest = SmtpDestination(address, server, port, user, password)
        return cls(cargo, source, dest)

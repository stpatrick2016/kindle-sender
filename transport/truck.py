from abc import ABC, abstractmethod
from contextlib import contextmanager
import tempfile
import os
import typing

from .exceptions import CargoEmptyError, CargoLostError

class Cargo(ABC):
    
    @contextmanager
    @abstractmethod
    def fill(self) -> any:
        raise NotImplementedError

    @contextmanager
    @abstractmethod
    def empty(self) -> any:
        raise NotImplementedError

class Source(ABC):

    @abstractmethod
    async def load(self, cargo: Cargo):
        pass

class Destination(ABC):
    
    @abstractmethod
    async def unload(self, cargo: Cargo):
        pass

class Truck:
    def __init__(self, source: Source, destination: Destination):
        self._source = source
        self._dest = destination

    async def deliver(self, cargo: Cargo):
        await self._source.load(cargo)
        await self._dest.unload(cargo)

class GroundedCargo(Cargo):

    _temp_file_path: str

    @contextmanager
    def fill(self) -> typing.BinaryIO:
        fd, self._temp_file_path = tempfile.mkstemp()
        file = os.fdopen(fd, "wb")
        yield file
        file.close()

    @contextmanager
    def empty(self) -> typing.BinaryIO:
        if self._temp_file_path is None:
            raise CargoEmptyError
        if not os.path.isfile(self._temp_file_path):
            raise CargoLostError
        f = open(self._temp_file_path, "rb")
        yield f
        f.close()
        os.remove(self._temp_file_path)
        self._temp_file_path = None

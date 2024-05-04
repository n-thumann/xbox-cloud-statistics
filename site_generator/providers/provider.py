from abc import ABCMeta, abstractmethod
from pathlib import Path

import httpx


class Provider(metaclass=ABCMeta):
    cache = Path(".cache")

    def __init__(self):
        self.cache.mkdir(exist_ok=True)

    @abstractmethod
    def get(self): ...

    def _download(self, file_name: str, remote_file_url: str):
        file = self.cache / file_name
        if not file.exists():
            response = httpx.get(remote_file_url)
            response.raise_for_status()

            file.write_bytes(response.read())

        return file.read_bytes()

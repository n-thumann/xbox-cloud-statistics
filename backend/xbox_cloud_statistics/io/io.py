from abc import ABC, abstractmethod

from xbox_cloud_statistics.models import Results


class IO(ABC):
    @staticmethod
    @abstractmethod
    def handle(results: Results):
        pass

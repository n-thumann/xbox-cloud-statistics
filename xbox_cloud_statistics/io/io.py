from abc import ABC, abstractmethod

from common.models import Results


class IO(ABC):
    @staticmethod
    @abstractmethod
    def handle(results: Results):
        pass

from abc import ABC, abstractmethod


class GraphStorageOutputPort(ABC):
    def save(self, name: str, data: bytes):
        pass

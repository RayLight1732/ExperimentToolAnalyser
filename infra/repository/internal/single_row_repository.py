from typing import TypeVar,Generic,List
from abc import ABC,abstractmethod
from infra.file_system.path_resolver import PathResolver
from infra.file_system.file_system import FileSystem

TDomain = TypeVar("TDomain")

class SingleRowCsvRepository(ABC, Generic[TDomain]):
    def __init__(self, path_resolver:PathResolver, file_system:FileSystem):
        self.path_resolver = path_resolver
        self.file_system = file_system

    def _load_single_row(self, path: str) -> TDomain:
        for row in self.file_system.load_csv(path):
            return self._to_domain(row)
        raise self._not_found_error(path)

    @abstractmethod
    def _to_domain(self, row) -> TDomain:
        pass

    @abstractmethod
    def _not_found_error(self, path: str) -> Exception:
        pass
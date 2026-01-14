from domain.value.laveled_value import LaveledValues
from domain.repository.laveled_value_repository import (
    LaveledValueRepository as ILaveledValueRepository,
)
from infra.file_system.file_system import FileSystem
from typing import Generator, List, Any
from infra.file_system.path_resolver import PathResolver
from itertools import zip_longest


class LaveledValueRepository(ILaveledValueRepository):
    def __init__(self, path_resolver: PathResolver, file_system: FileSystem) -> None:
        self.path_resolver = path_resolver
        self.file_system = file_system

    def save(self, name: str, values: List[LaveledValues]):
        self.file_system.save_csv(
            self.path_resolver.save_path(name), self._generate(values)
        )

    def _generate(
        self, values: List[LaveledValues]
    ) -> Generator[List[str], None, None]:
        for value in values:
            yield [laveled_value.lavel for laveled_value in value.values]

            value_lists: List[List[Any]] = [
                laveled_value.value for laveled_value in value.values
            ]

            for row in zip_longest(*value_lists, fillvalue=""):
                yield [str(v) for v in row]

            yield [""]

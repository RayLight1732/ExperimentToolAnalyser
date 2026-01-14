from domain.value.laveled_value import LaveledValues
from domain.repository.inferential_result_repository import (
    InferentialResultRepository as IInferentialResultRepository,
)
from domain.analysis.inferential.result.inferential_result_history import (
    InferentialResultHistory,
)
from domain.analysis.inferential.result.inferential_result import InferentialResult
from infra.file_system.file_system import FileSystem
from typing import Generator, List, Any
from infra.file_system.path_resolver import PathResolver
from itertools import zip_longest


class InferentialResultRepository(IInferentialResultRepository):
    def __init__(self, path_resolver: PathResolver, file_system: FileSystem) -> None:
        self.path_resolver = path_resolver
        self.file_system = file_system

    def save(self, name: str, result: InferentialResultHistory):
        self.file_system.save_csv(
            self.path_resolver.save_path(name),
            self._generate_inferential_result_history(result),
        )

    def _generate_inferential_result_history(
        self, result: InferentialResultHistory
    ) -> Generator[List[str], None, None]:
        yield ["original"]
        for value in self._generate_inferential_result(result.original):
            yield value

        for post_process_result in result.post_process:
            yield [""]
            yield [post_process_result.method]
            for value in self._generate_inferential_result(result.original):
                yield value

    def _generate_inferential_result(
        self, result: InferentialResult
    ) -> Generator[List[str], None, None]:
        for comparison, evidence in result.comparisons.items():
            yield [str(comparison.left), str(comparison.right), str(evidence.p_value)]

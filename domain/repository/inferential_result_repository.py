from abc import ABC, abstractmethod
from domain.analysis.inferential.result.inferential_result_history import (
    InferentialResultHistory,
)


class InferentialResultRepository(ABC):
    @abstractmethod
    def save(self, name: str, result: InferentialResultHistory):
        pass

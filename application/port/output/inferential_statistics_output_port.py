from abc import ABC, abstractmethod
from domain.analysis.inferential.result.inferential_result_history import (
    InferentialResultHistory,
)
from typing import List
from domain.value.subject import Subject


class InferentialResultOutputPort(ABC):
    @abstractmethod
    def present(
        self, subjects: List[Subject], result: InferentialResultHistory
    ) -> None:
        pass

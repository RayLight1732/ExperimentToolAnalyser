from domain.analysis.inferential.result.inferential_result import InferentialResult
from typing import List
from abc import ABC, abstractmethod


class ResultOutputPort(ABC):
    @abstractmethod
    def output(self, result: List[InferentialResult]) -> None:
        pass

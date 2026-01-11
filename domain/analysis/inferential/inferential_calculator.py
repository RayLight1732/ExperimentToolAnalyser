from abc import ABC, abstractmethod
from domain.analysis.inferential.result.inferential_result import InferentialResult
from domain.value.grouped_value import GroupedValue


class InferentialCalculator(ABC):
    @abstractmethod
    def calculate(self, grouped: GroupedValue) -> InferentialResult:
        pass

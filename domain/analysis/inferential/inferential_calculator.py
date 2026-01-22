from abc import ABC, abstractmethod
from domain.analysis.inferential.result.inferential_result import InferentialResult
from domain.value.grouped_value import GroupedValue
from typing import Set
from domain.value.condition import Condition

class InferentialCalculator(ABC):
    @abstractmethod
    def calculate(self, grouped: GroupedValue,target:Set[Condition]) -> InferentialResult:
        pass

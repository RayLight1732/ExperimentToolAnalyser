from abc import ABC,abstractmethod
from domain.statistics.inferential.result.statistical_result import StatisticalResult
from domain.value.grouped_value import GroupedValue

class InferentialCalculator(ABC):
    @abstractmethod
    def calculate(self, grouped: GroupedValue) -> StatisticalResult:
        pass
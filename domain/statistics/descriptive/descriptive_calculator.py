from abc import ABC,abstractmethod
from domain.value.grouped_value import GroupedValue
from domain.statistics.descriptive.result.descriptive_result import DescriptiveResult

class DescriptiveCalculator(ABC):
    @abstractmethod
    def calculate(
        self,
        grouped: GroupedValue
    ) -> DescriptiveResult:
        pass
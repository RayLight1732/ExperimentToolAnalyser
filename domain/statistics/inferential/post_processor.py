from abc import ABC,abstractmethod
from domain.statistics.inferential.result.statistical_result import StatisticalResult

class PostProcessor(ABC):
    @abstractmethod
    def process(
        self,
        result: StatisticalResult
    ) -> StatisticalResult:
        pass
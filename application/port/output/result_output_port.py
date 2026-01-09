from domain.statistics.inferential.result.statistical_result import StatisticalResult
from typing import List
from abc import ABC,abstractmethod


class ResultOutputPort(ABC):
    @abstractmethod
    def output(self, result: List[StatisticalResult]) -> None:
        pass
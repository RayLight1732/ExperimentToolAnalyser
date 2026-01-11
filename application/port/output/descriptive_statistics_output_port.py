from abc import ABC, abstractmethod
from domain.analysis.descriptive.result.descriptive_result import DescriptiveResult
from typing import List
from domain.value.subject import Subject


class DescriptiveStatisticsOutputPort(ABC):

    @abstractmethod
    def present(self, subjects: List[Subject], result: DescriptiveResult) -> None:
        pass

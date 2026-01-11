from domain.analysis.descriptive.result.descriptive_result import DescriptiveResult
from domain.value.subject import Subject
from abc import ABC, abstractmethod


# TODO fix signature
class DescriptiveStatisticsInputPort(ABC):

    @abstractmethod
    def execute(self, subjects: list[Subject]) -> DescriptiveResult:
        pass

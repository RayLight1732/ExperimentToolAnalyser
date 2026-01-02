from domain.entity.subject import Subject
from domain.value_object.grouped_value import GroupedValue
from abc import ABC, abstractmethod
from typing import List


class Collector(ABC):
    @abstractmethod
    def collect(self, subjects: List[Subject]) -> GroupedValue[float]:
        pass

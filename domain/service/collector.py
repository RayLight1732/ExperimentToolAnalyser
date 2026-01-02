from domain.entity.subject import Subject
from domain.value_object.grouped_value import GroupedValue
from abc import ABC, abstractmethod
from typing import List, Generic, TypeVar

T = TypeVar("T")


class Collector(ABC, Generic[T]):
    @abstractmethod
    def collect(self, subjects: List[Subject]) -> GroupedValue[T]:
        pass

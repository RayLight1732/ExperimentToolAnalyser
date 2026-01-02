from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from domain.value_object.grouped_value import GroupedValue

T = TypeVar("T")


class Calculator(ABC, Generic[T]):
    @abstractmethod
    def calculate(self, collected: GroupedValue[float]) -> T:
        pass

from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from domain.value_object.grouped_value import GroupedValue

T = TypeVar("T")
U = TypeVar("U")


class Calculator(ABC, Generic[T, U]):
    @abstractmethod
    def calculate(self, collected: GroupedValue[T]) -> U:
        pass

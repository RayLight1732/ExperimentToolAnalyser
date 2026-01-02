from abc import ABC, abstractmethod
from domain.value_object.condition import Condition
from usecase.grouped_value import GroupedValue
from typing import Dict,Generic, TypeVar

T = TypeVar("T")
U = TypeVar("U")

class Calculator(ABC,Generic[T,U]):
    @abstractmethod
    def calculate(
        self,
        collected: GroupedValue[T]
    ) -> U:
        pass
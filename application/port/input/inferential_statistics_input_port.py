from typing import Set
from domain.value.condition import Condition
from application.model.value_type import ValueType
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

TOption = TypeVar("TOption")



class InferentialStatisticsInputPort(Generic[TOption],ABC):
    @abstractmethod
    def execute(self, type: ValueType, filter: bool,option:TOption) -> None:
        pass

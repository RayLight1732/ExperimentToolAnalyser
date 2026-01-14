from typing import Set
from domain.value.condition import Condition
from application.model.value_type import ValueType
from abc import ABC, abstractmethod


class InferentialStatisticsInputPort(ABC):
    @abstractmethod
    def execute(self, type: ValueType) -> None:
        pass

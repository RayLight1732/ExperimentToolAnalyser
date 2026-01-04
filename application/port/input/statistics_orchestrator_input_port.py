from abc import ABC, abstractmethod
from application.dto.value_type import ValueType
from typing import List


class StatisticsOrchestratorInputPort(ABC):
    @abstractmethod
    def execute(
        self,
        value_types: List[ValueType],
    ) -> None:
        pass

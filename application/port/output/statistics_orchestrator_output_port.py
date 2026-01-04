from abc import ABC, abstractmethod
from application.dto.value_type import ValueType
from typing import Dict, Any


class StatisticsOrchestratorOutputPort(ABC):

    @abstractmethod
    def on_start(self, value_type: ValueType) -> None:
        pass

    @abstractmethod
    def on_progress(
        self,
        value_type: ValueType,
        current: int,
        total: int,
    ) -> None:
        pass

    @abstractmethod
    def on_complete(
        self,
        result: Dict[ValueType, Any],
    ) -> None:
        pass

    @abstractmethod
    def on_error(
        self,
        value_type: ValueType,
        error: Exception,
    ) -> None:
        pass

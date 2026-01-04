from abc import ABC, abstractmethod
from application.dto.value_type import ValueType
from typing import List, Optional
from application.dto.filter_parameter import FilterParameter


class StatisticsOrchestratorInputPort(ABC):
    @abstractmethod
    def execute(
        self,
        value_types: List[ValueType],
        filter_parameter: Optional[FilterParameter],
    ) -> None:
        pass

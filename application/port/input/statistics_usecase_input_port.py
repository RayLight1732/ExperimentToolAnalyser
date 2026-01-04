from abc import ABC, abstractmethod
from domain.value_object.grouped_value import GroupedValue
from application.dto.value_type import ValueType


class StatisticsUsecaseInputPort(ABC):
    @abstractmethod
    def execute(
        self,
        value_type: ValueType,
        values: GroupedValue,
    ) -> None:
        pass

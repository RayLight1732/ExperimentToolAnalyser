from abc import ABC, abstractmethod
from application.dto.value_type import ValueType
from domain.value_object.grouped_value import GroupedValue


class CollectValueOutputPort(ABC):

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
        value_type: ValueType,
        result: GroupedValue[float],
    ) -> None:
        pass

    @abstractmethod
    def on_error(
        self,
        value_type: ValueType,
        error: Exception,
    ) -> None:
        pass

from abc import ABC, abstractmethod
from application.dto.rm_anova_result_dto import RMAnovaResult
from application.dto.value_type import ValueType


class RunRMAnovaOutputPort(ABC):

    @abstractmethod
    def on_start(self, value_type: ValueType) -> None:
        pass

    @abstractmethod
    def on_complete(
        self,
        value_type: ValueType,
        result: RMAnovaResult,
    ) -> None:
        pass

    @abstractmethod
    def on_error(
        self,
        value_type: ValueType,
        error: Exception,
    ) -> None:
        pass

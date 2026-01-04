from abc import ABC, abstractmethod
from application.dto.t_test_result_dto import CorrectedAndOriginalValueByConditionPair
from application.dto.value_type import ValueType


class RunPairedTTestWithHolmOutputPort(ABC):

    @abstractmethod
    def on_start(self, value_type: ValueType) -> None:
        pass

    @abstractmethod
    def on_complete(
        self,
        value_type: ValueType,
        result: CorrectedAndOriginalValueByConditionPair,
    ) -> None:
        pass

    @abstractmethod
    def on_error(
        self,
        value_type: ValueType,
        error: Exception,
    ) -> None:
        pass

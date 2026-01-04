from domain.value_object.grouped_value import GroupedValue
from abc import ABC, abstractmethod
from typing import Any


class Filter(ABC):
    # def calculate(self, collected: GroupedValue[LaveledValue]) -> T:
    #     pass
    @abstractmethod
    def filter(self, values: GroupedValue[float], param: Any) -> GroupedValue[float]:
        pass

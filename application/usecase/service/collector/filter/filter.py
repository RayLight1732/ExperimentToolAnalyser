from domain.value_object.grouped_value import GroupedValue
from abc import ABC, abstractmethod
from typing import Any


class Filter(ABC):
    @abstractmethod
    def filter(self, values: GroupedValue, param: Any) -> GroupedValue:
        pass

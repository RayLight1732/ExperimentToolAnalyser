from abc import ABC, abstractmethod
from domain.value.grouped_value import GroupedValue

class ValueFilter(ABC):
    @abstractmethod
    def apply(self, grouped: GroupedValue) -> GroupedValue:
        pass

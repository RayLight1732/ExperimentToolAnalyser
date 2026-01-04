from abc import ABC, abstractmethod
from domain.value_object.grouped_value import GroupedValue
from application.dto.value_type import ValueType
from domain.entity.subject import Subject
from typing import List


class CollectValueInputPort(ABC):
    @abstractmethod
    def execute(
        self,
        subjects: List[Subject],
        value_type: ValueType,
    ) -> GroupedValue[float]:
        pass

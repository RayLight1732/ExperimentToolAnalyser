from abc import ABC, abstractmethod
from domain.value_object.grouped_value import GroupedValue
from application.dto.value_type import ValueType
from application.dto.filter_parameter import FilterParameter
from domain.entity.subject import Subject
from typing import List, Optional


class CollectValueInputPort(ABC):
    @abstractmethod
    def execute(
        self,
        subjects: List[Subject],
        value_type: ValueType,
        filter_parameter: Optional[FilterParameter],
    ) -> GroupedValue[float]:
        pass

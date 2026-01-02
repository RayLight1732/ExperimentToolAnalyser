from dataclasses import dataclass
from domain.value_object.condition import Condition
from domain.value_object.subject_data import SubjectData
from typing import Dict,Generic, TypeVar


T = TypeVar("T")

@dataclass
class GroupedValue(Generic[T]):
    value: Dict[Condition,Dict[SubjectData,T]]

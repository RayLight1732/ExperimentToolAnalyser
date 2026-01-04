from dataclasses import dataclass
from domain.value_object.condition import Condition
from domain.value_object.subject_data import SubjectData
from typing import Dict


@dataclass(frozen=True)
class GroupedValue:
    name: str
    value: Dict[Condition, Dict[SubjectData, float]]

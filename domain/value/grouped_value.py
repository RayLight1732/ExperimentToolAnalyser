from dataclasses import dataclass
from domain.value.condition import Condition
from domain.value.subject_data import SubjectData
from typing import Dict


@dataclass(frozen=True)
class GroupedValue:
    name: str
    value: Dict[Condition, Dict[SubjectData, float]]

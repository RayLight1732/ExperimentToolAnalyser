from domain.value.ssq import SSQ
from domain.value.fms import FMS
from domain.value.body_sway import BodySway
from domain.value.condition import Condition
from domain.value.time_point import TimePoint
from domain.value.subject_data import SubjectData
import dataclasses
from typing import Dict, List, Set
from datetime import datetime


@dataclasses.dataclass
class TrialResult:
    ssq: Dict[TimePoint, SSQ]
    fms: FMS
    body_sway: BodySway


@dataclasses.dataclass
class TrialResultSummary:
    ssq_timestamp: Dict[TimePoint, datetime]
    fms_timestamp: datetime
    body_sway_timestamp: datetime


@dataclasses.dataclass
class Session:
    condition: Condition
    result: TrialResultSummary


@dataclasses.dataclass
class Subject:
    data: SubjectData
    sessions: List[Session]

    def completed(self, required: Set[Condition]) -> bool:
        condition_set: Set[Condition] = set()
        for session in self.sessions:
            condition_set.add(session.condition)
        # 被りがなく、requiredがすべて含まれている場合true
        return len(condition_set) == len(self.sessions) and required.issubset(condition_set)

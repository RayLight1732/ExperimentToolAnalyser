from domain.value_object.ssq import SSQ
from domain.value_object.fms import FMS
from domain.value_object.body_sway import BodySway
from domain.value_object.condition import Condition
from domain.value_object.time_point import TimePoint
from domain.value_object.subject_data import SubjectData
import dataclasses
from typing import Dict, List
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

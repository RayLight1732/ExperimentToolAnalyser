from datetime import datetime
from dataclasses import dataclass
from typing import List
from enum import Enum


class FileKind(Enum):
    SSQ_BEFORE = True
    SSQ_AFTER = True
    FMS = True
    BODY_SWAY = False

    def __init__(self, is_questionnaire: bool):
        super().__init__()
        self.is_questionnaire = is_questionnaire


@dataclass(frozen=True)
class ExperimentFile:
    path: str
    kind: FileKind
    time_stamp: datetime


@dataclass(frozen=True)
class SessionFileCandidates:
    files: List[ExperimentFile]

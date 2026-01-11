from domain.value.subject_data import SubjectData
from domain.value.condition import Condition
from datetime import datetime


class BodySwayFormatError(Exception):
    def __init__(
        self, subject_data: SubjectData, condition: Condition, timestamp: datetime
    ):
        super().__init__(
            f"Body sway format is invalid: {subject_data} {condition} {timestamp}"
        )

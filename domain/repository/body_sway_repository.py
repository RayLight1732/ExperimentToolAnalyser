from abc import ABC, abstractmethod
from domain.value.body_sway import BodySway
from domain.value.condition import Condition
from datetime import datetime
from domain.value.subject_data import SubjectData


class BodySwayRepository(ABC):
    @abstractmethod
    def load(
        self, subject_data: SubjectData, condition: Condition, timestamp: datetime
    ) -> BodySway:
        pass

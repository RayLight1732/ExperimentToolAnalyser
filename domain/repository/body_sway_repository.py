from abc import ABC, abstractmethod
from domain.value_object.body_sway import BodySway
from domain.value_object.condition import Condition
from datetime import datetime
from domain.value_object.subject_data import SubjectData


class BodySwayRepository(ABC):
    @abstractmethod
    def load(
        self, subject_data: SubjectData, condition: Condition, timestamp: datetime
    ) -> BodySway:
        pass

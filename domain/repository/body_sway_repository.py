from abc import ABC, abstractmethod
from domain.value_object.body_sway import BodySway
from domain.value_object.condition import Condition
from datetime import datetime


class BodySwayRepository(ABC):
    @abstractmethod
    def load(self, name: str, condition: Condition, timestamp: datetime) -> BodySway:
        pass

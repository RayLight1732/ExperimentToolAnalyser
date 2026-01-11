from abc import ABC, abstractmethod
from domain.value.subject import Session
from domain.value.condition import Condition


class SessionRepository(ABC):
    @abstractmethod
    def get_session(self, name: str, condition: Condition) -> Session:
        pass

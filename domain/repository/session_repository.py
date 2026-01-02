from abc import ABC,abstractmethod
from domain.entity.subject import Session
from domain.value_object.condition import Condition
class SessionRepository(ABC):
    @abstractmethod
    def get_session(self,name:str,condition:Condition)->Session:
        pass
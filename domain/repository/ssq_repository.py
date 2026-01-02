from abc import ABC,abstractmethod
from domain.value_object.ssq import SSQ
from domain.value_object.condition import Condition
from domain.value_object.time_point import TimePoint
from datetime import datetime

class SSQRepository(ABC):
    @abstractmethod
    def get_ssq(self,name:str,condition:Condition,time_point:TimePoint,timestamp:datetime)->SSQ:
        pass
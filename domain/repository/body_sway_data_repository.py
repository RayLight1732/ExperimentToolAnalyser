from abc import ABC,abstractmethod
from domain.value_object.body_sway_data import BodySwayData
from domain.value_object.condition import Condition
from datetime import datetime

class BodySwayDataRepository(ABC):
    @abstractmethod
    def load(self,name:str,condition:Condition,timestamp:datetime)->BodySwayData:
        pass
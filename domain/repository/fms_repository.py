from abc import ABC,abstractmethod
from domain.value_object.fms import FMS
from domain.value_object.condition import Condition
from datetime import datetime
class FMSRepository(ABC):

    @abstractmethod
    def get_fms(self,name:str,condition:Condition,timestamp:datetime)->FMS:
        pass
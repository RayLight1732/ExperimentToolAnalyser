from abc import ABC,abstractmethod
from domain.value_object.condition import Condition
from domain.entity.subject import Subject
from typing import List,Dict,Tuple
from collections import defaultdict
from domain.service.collector import Collector

class CollectAllValueUsecaseInterface(ABC):
    @abstractmethod
    def execute(self,subjects:List[Subject])->Dict[Condition,List[List[float]]]:
        pass

class CollectAllValueUsecase(CollectAllValueUsecaseInterface):
    def __init__(self,collectors:List[Collector]):
        super().__init__()
        self.collectors = collectors

    def execute(self,subjects:List[Subject])->Dict[Condition,List[List[float]]]:
        result = defaultdict(lambda:list())
        for collector in self.collectors:
            grouped_value = collector.collect(subjects)
            for condition,value in grouped_value.value.items():
                result[condition].append([v for v in value.values()])
        return dict(result)
        
        


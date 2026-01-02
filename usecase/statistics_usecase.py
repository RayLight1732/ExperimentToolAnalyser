from abc import ABC,abstractmethod
from typing import List,Dict,Generic,TypeVar
from domain.entity.subject import Subject
from domain.value_object.condition import Condition
from domain.service.calculator import Calculator
from domain.service.collector import Collector
from collections import defaultdict
T = TypeVar("T")
U = TypeVar("U")

class StatisticsUsecaseInterface(ABC,Generic[T]):
    @abstractmethod
    def execute(self,subjects:List[Subject])->T:
        pass

class StatisticsUsecase(Generic[T,U],StatisticsUsecaseInterface[U]):

    def __init__(self,collector:Collector[T],calculator:Calculator[T,U]):
        self.collector = collector
        self.calculator = calculator

    def execute(self,subjects:List[Subject])->U:
        collected = self.collector.collect(subjects)
        return self.calculator.calculate(collected)
    
# class MassStatisticsUsecase(Generic[T,U],StatisticsUsecaseInterface[U]):

#     def __init__(self,collectors:List[Collector[T]],calculator:Calculator[T,U]):
#         self.collectors = collectors
#         self.calculator = calculator

#     def execute(self,subjects:List[Subject])->Dict[Condition,List[U]]:
#         results = defaultdict(lambda:list())
#         for collector in self.collectors:
#             collected = collector.collect(subjects)
#             calculated = self.calculator.calculate(collected)
#             for condition,value in calculated.items():
#                 results[condition].append(value)

#         return results



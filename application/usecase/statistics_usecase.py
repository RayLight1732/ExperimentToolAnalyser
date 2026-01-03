from abc import ABC, abstractmethod
from typing import List, Any
from domain.entity.subject import Subject
from usecase.service.operation_registory import (
    OperationRegistory,
    ValueType,
    CalculationType,
)


class StatisticsUsecaseInterface(ABC):
    @abstractmethod
    def execute(
        self,
        subjects: List[Subject],
        value_type: ValueType,
        calculation_type: CalculationType,
    ) -> Any:
        pass


class StatisticsUsecase(StatisticsUsecaseInterface):

    def __init__(self, registory: OperationRegistory):
        self.registory = registory

    def execute(
        self,
        subjects: List[Subject],
        value_type: ValueType,
        calculation_type: CalculationType,
    ) -> Any:
        operation = self.registory.get_operation(value_type, calculation_type)
        return operation.execute(subjects)


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

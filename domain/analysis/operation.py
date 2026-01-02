from domain.service.collector import Collector
from domain.service.calculator import Calculator
from domain.entity.subject import Subject
from typing import List, TypeVar, Generic

T = TypeVar("T")


class Operation(Generic[T]):
    def __init__(self, collector: Collector, calculator: Calculator[T]):
        self.collector = collector
        self.calculator = calculator

    def execute(self, subjects: List[Subject]) -> T:
        collected = self.collector.collect(subjects)
        return self.calculator.calculate(collected)

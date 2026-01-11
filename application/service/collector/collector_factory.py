from abc import ABC, abstractmethod
from application.model.value_type import ValueType
from application.service.collector.collector import Collector
from typing import Dict


# TODO 命名?
class CollectorFactory(ABC):
    @abstractmethod
    def get(self, value_type: ValueType) -> Collector:
        pass


class CollectorFactoryImpl(CollectorFactory):
    def __init__(self, collectors: Dict[ValueType, Collector]) -> None:
        self.collectors = collectors

    def get(self, value_type: ValueType) -> Collector:
        return self.collectors[value_type]

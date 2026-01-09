from abc import ABC, abstractmethod
from application.model.value_type import ValueType
from application.usecase.service.collector.collector import Collector


class CollectorFactory(ABC):
    @abstractmethod
    def get(self, value_type: ValueType) -> Collector:
        pass

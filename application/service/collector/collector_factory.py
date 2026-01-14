from abc import ABC, abstractmethod
from application.model.value_type import ValueType
from application.service.collector.collector import Collector


# TODO 命名?
class CollectorFactory(ABC):
    @abstractmethod
    def get(self, value_type: ValueType) -> Collector:
        pass

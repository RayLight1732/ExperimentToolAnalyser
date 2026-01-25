from abc import ABC, abstractmethod
from application.port.output.progress_output_port import ProgressAdvanceOutputPort
from domain.value.subject import Subject
from domain.value.grouped_value import GroupedValue
from typing import Set
from domain.value.condition import Condition

class Collector(ABC):
    @abstractmethod
    def collect(self, subjects: list[Subject],target:Set[Condition], filter=False) -> GroupedValue:
        pass

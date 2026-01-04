from abc import ABC, abstractmethod
from typing import List
from domain.entity.subject import Subject


class ListCompletedSubjectInputPort(ABC):
    @abstractmethod
    def execute(self) -> List[Subject]:
        pass

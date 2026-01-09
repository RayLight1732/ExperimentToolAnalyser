from abc import ABC,abstractmethod
from typing import Sequence,Set
from domain.subject import Subject
from domain.value.condition import Condition


class SubjectRepository(ABC):
    @abstractmethod
    def list_subjects(self)->Sequence[Subject]:
        pass

    @abstractmethod
    def list_completed_subjects(self,required:Set[Condition]) -> Sequence[Subject]:
        pass
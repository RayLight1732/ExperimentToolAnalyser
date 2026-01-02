from abc import ABC,abstractmethod
from typing import Sequence
from domain.entity.subject import Subject
class SubjectRepository(ABC):
    @abstractmethod
    def list_subjects(self)->Sequence[Subject]:
        pass
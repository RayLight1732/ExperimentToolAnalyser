from abc import ABC, abstractmethod
from typing import Sequence
from domain.value.subject import Subject


class SubjectRepository(ABC):
    @abstractmethod
    def list_subjects(self) -> Sequence[Subject]:
        pass

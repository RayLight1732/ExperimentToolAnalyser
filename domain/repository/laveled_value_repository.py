from abc import ABC, abstractmethod
from domain.value_object.laveled_value import LaveledValues
from typing import List


class LaveledValueRepository(ABC):
    @abstractmethod
    def save(self, name: str, values: List[LaveledValues]):
        pass

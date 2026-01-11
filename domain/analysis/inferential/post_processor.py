from abc import ABC, abstractmethod
from domain.analysis.inferential.result.inferential_result import InferentialResult


class PostProcessor(ABC):
    @abstractmethod
    def process(self, result: InferentialResult) -> InferentialResult:
        pass

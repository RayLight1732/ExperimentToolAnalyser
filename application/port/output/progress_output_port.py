from abc import ABC, abstractmethod
from application.dto.progress_phase import ProgressPhase
from application.dto.inferential_analysis_step import InferentialAnalysisStep


class ProgressAdvanceOutputPort(ABC):
    @abstractmethod
    def on_advanced(self, phase: ProgressPhase, current: int, total: int):
        pass


class ProgressLifeCycleOutputPort(ABC):
    @abstractmethod
    def on_started(self, category: InferentialAnalysisStep):
        pass

    @abstractmethod
    def on_finished(self, category: InferentialAnalysisStep):
        pass

    @abstractmethod
    def on_error(self, exception: Exception):
        pass

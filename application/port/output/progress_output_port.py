from abc import ABC,abstractmethod
from application.model.progress_phase import ProgressPhase
from application.model.processing_category import ProcessingCategory

class ProgressAdvanceOutputPort(ABC):
    @abstractmethod
    def on_advanced(self, pahse:ProgressPhase,current: int, total: int):
        pass

class ProgressLifeCycleOutPutPort(ABC):
    @abstractmethod
    def on_started(self,category:ProcessingCategory):
        pass

    @abstractmethod
    def on_finished(self,category:ProcessingCategory):
        pass

    @abstractmethod
    def on_error(self,exception:Exception):
        pass
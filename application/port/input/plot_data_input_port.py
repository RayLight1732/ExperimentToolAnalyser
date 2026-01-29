from abc import ABC, abstractmethod
from application.model.graph_options import GraphOption
from application.model.graph_type import GraphType
from application.model.value_type import ValueType


class PlotDataInputPort(ABC):
    @abstractmethod
    def execute(
        self,
        value_type: ValueType,
        graph_title: str,
        graph_type: GraphType,
        option: GraphOption,
        filter: bool,
    ):
        pass

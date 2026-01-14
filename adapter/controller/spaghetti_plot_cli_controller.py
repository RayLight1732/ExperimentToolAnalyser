from application.model.graph_options import GraphOptions
from adapter.utils import parse_value_type_str
from typing import Callable
from application.port.input.plot_data_input_port import PlotDataInputPort
from application.model.graph_type import GraphType
from application.port.output.progress_output_port import (
    ProgressAdvanceOutputPort,
    ProgressLifeCycleOutputPort,
)
from adapter.presenter.progress_presenter import ProgressPresenter


class SpaghettiPlotCLIController:
    def __init__(
        self,
        usecase_factory: Callable[
            [
                ProgressLifeCycleOutputPort,
                ProgressAdvanceOutputPort,
            ],
            PlotDataInputPort,
        ],
    ):
        self.usecase_factory = usecase_factory

    def handle(self, input_line: str):
        value_type = parse_value_type_str(input_line)

        # TODO DIする
        progress_presenter = ProgressPresenter()
        usecase = self.usecase_factory(
            progress_presenter,
            progress_presenter,
        )
        usecase.execute(
            value_type,
            value_type.name,
            GraphType.SPAGHETTI,
            GraphOptions(x_label="Condition", y_label=value_type.name),
        )

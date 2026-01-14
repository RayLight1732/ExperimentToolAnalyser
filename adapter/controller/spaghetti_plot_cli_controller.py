from application.model.graph_options import GraphOptions
from adapter.utils import parse_value_type_str, parse_bool
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
        tokens = input_line.split()
        value_type = parse_value_type_str(tokens[0])
        filter = parse_bool(tokens[1])

        # TODO DIする
        progress_presenter = ProgressPresenter()
        usecase = self.usecase_factory(
            progress_presenter,
            progress_presenter,
        )
        title = value_type.name
        if filter:
            title += "_filtered"
        usecase.execute(
            value_type,
            title,
            GraphType.SPAGHETTI,
            GraphOptions(x_label="Condition", y_label=value_type.name),
            filter,
        )

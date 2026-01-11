from application.model.value_type import ValueType
from presentation.cli.utils import parse_value_type_str
from typing import Callable
from application.port.input.inferential_statistics_input_port import (
    InferentialStatisticsInputPort,
)
from application.port.output.progress_output_port import (
    ProgressAdvanceOutputPort,
    ProgressLifeCycleOutputPort,
)
from application.port.output.inferential_statistics_output_port import (
    InferentialResultOutputPort,
)
from presentation.cli.presenter.inferential_result_presenter import (
    InferentialResultPresenter,
)
from presentation.cli.presenter.progress_presenter import ProgressPresenter


class InferentialStatisticsCLIController:
    def __init__(
        self,
        usecase_factory: Callable[
            [
                ProgressLifeCycleOutputPort,
                ProgressAdvanceOutputPort,
                InferentialResultOutputPort,
            ],
            InferentialStatisticsInputPort,
        ],
    ):
        self.usecase_factory = usecase_factory

    def handle(self, input_line: str):
        value_type = parse_value_type_str(input_line)
        progress_presenter = ProgressPresenter()
        usecase = self.usecase_factory(
            progress_presenter,
            progress_presenter,
            InferentialResultPresenter(),
        )
        usecase.execute(type=value_type)

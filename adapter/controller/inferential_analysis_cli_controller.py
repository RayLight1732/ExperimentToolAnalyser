from application.model.value_type import ValueType
from adapter.utils import parse_value_type_str, parse_bool
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
from adapter.presenter.inferential_result_presenter import (
    InferentialResultPresenter,
)
from adapter.presenter.progress_presenter import ProgressPresenter
from domain.repository.inferential_result_repository import InferentialResultRepository


class InferentialStatisticsCLIController:
    def __init__(
        self,
        repository: InferentialResultRepository,  # TODO どうにかする
        usecase_factory: Callable[
            [
                ProgressLifeCycleOutputPort,
                ProgressAdvanceOutputPort,
                InferentialResultOutputPort,
            ],
            InferentialStatisticsInputPort,
        ],
    ):
        self.repository = repository
        self.usecase_factory = usecase_factory

    def handle(self, input_line: str):
        tokens = input_line.split()
        value_type = parse_value_type_str(tokens[0])
        filter = parse_bool(tokens[1])

        file_name = value_type.name
        if filter:
            file_name += "_filtered"
        file_name += ".csv"
        progress_presenter = ProgressPresenter()
        usecase = self.usecase_factory(
            progress_presenter,
            progress_presenter,
            InferentialResultPresenter(file_name, self.repository),
        )
        usecase.execute(type=value_type, filter=filter)

from application.port.output.progress_output_port import ProgressAdvanceOutputPort
from application.service.collector.collector import Collector
from domain.analysis.descriptive.descriptive_calculator import DescriptiveCalculator
from domain.analysis.descriptive.result.descriptive_result import DescriptiveResult
from domain.value.subject import Subject
from application.port.input.descriptive_statistics_input_port import (
    DescriptiveStatisticsInputPort,
)


# TODO fix signature
class RunDescriptiveStatisticsUseCase(DescriptiveStatisticsInputPort):
    def __init__(
        self,
        collector: Collector,
        descriptive_calculator: DescriptiveCalculator,
    ):
        self.collector = collector
        self.descriptive_calculator = descriptive_calculator

    def execute(
        self,
        subjects: list[Subject],
    ) -> DescriptiveResult:
        grouped = self.collector.collect(subjects)
        return self.descriptive_calculator.calculate(grouped)

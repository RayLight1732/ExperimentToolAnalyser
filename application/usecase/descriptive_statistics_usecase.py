from application.port.output.progress_output_port import ProgressAdvanceOutputPort
from application.usecase.service.collector.collector import Collector
from domain.statistics.descriptive.descriptive_calculator import DescriptiveCalculator
from domain.statistics.descriptive.result.descriptive_result import DescriptiveResult
from domain.subject import Subject

class DescriptiveStatisticsUseCase:
    def __init__(
        self,
        collector: Collector,
        descriptive_calculator: DescriptiveCalculator,
    ):
        self.collector = collector
        self.descriptive_calculator = descriptive_calculator

    def execute(self, subjects: list[Subject],progress_advance_output_port:ProgressAdvanceOutputPort) -> DescriptiveResult:
        grouped = self.collector.collect(subjects,progress_advance_output_port)
        return self.descriptive_calculator.calculate(grouped)
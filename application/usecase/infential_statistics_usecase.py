from application.port.output.progress_output_port import ProgressAdvanceOutputPort, ProgressLifeCycleOutPutPort
from application.model.processing_category import ProcessingCategory
from typing import List

from application.usecase.service.collector.collector import Collector
from domain.statistics.inferential.result.statistical_result import StatisticalResult
from domain.statistics.inferential.result.statistical_result_history import StatisticalResultHistory
from domain.statistics.inferential.inferential_calculator import InferentialCalculator
from domain.statistics.inferential.post_processor import PostProcessor
from domain.subject import Subject
from domain.value.grouped_value import GroupedValue

class InfentialStatisticsUseCase:
    def __init__(
        self,
        collector: Collector,
        calculator: InferentialCalculator,
        post_processors: List[PostProcessor],
    ):
        self.collector = collector
        self.calculator = calculator
        self.post_processors = post_processors

    def execute(self, subjects: list[Subject],progress_cycle_output_port:ProgressLifeCycleOutPutPort,progress_advance_output_port:ProgressAdvanceOutputPort) -> StatisticalResultHistory:
        try:
            grouped = self._collect(subjects,progress_cycle_output_port,progress_advance_output_port)
            original = self._calculate(grouped,progress_cycle_output_port)
            post_process_results = self._post_process(original,progress_cycle_output_port)

            result = StatisticalResultHistory(original,post_process_results)

            return result
        except Exception as e:
            progress_cycle_output_port.on_error(e)
            raise

    def _collect(self,subjects:List[Subject],progress_cycle_output_port:ProgressLifeCycleOutPutPort,progress_advance_output_port:ProgressAdvanceOutputPort)->GroupedValue:
        progress_cycle_output_port.on_started(ProcessingCategory.COLLECT)
        grouped = self.collector.collect(subjects,progress_advance_output_port)
        progress_cycle_output_port.on_finished(ProcessingCategory.COLLECT)
        return grouped
    
    def _calculate(self,grouped:GroupedValue,progress_cycle_output_port:ProgressLifeCycleOutPutPort)->StatisticalResult:
        progress_cycle_output_port.on_started(ProcessingCategory.CALCULATE)
        original = self.calculator.calculate(grouped)
        progress_cycle_output_port.on_finished(ProcessingCategory.CALCULATE)
        return original
    
    def _post_process(self,original:StatisticalResult,progress_cycle_output_port:ProgressLifeCycleOutPutPort)->List[StatisticalResult]:
        post_process_results:List[StatisticalResult] = []

        progress_cycle_output_port.on_started(ProcessingCategory.POSTPROCESS)
        for post_processor in self.post_processors:
            original = post_processor.process(original)
            post_process_results.append(original)
        progress_cycle_output_port.on_finished(ProcessingCategory.POSTPROCESS)

        return post_process_results
    
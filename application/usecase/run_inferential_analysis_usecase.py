from application.model.inferential_analysis_step import InferentialAnalysisStep
from typing import Any, List, Set
from application.service.collector.collector import Collector
from domain.value.condition import Condition
from domain.repository.subject_repository import SubjectRepository
from domain.analysis.inferential.result.inferential_result import InferentialResult
from domain.analysis.inferential.result.inferential_result_history import (
    InferentialResultHistory,
)
from application.service.collector.collector_factory import CollectorFactory
from application.model.value_type import ValueType
from domain.analysis.inferential.inferential_calculator import InferentialCalculator
from domain.analysis.inferential.post_processor import PostProcessor
from domain.value.subject import Subject
from domain.value.grouped_value import GroupedValue
from application.port.output.inferential_statistics_output_port import (
    InferentialResultOutputPort,
)
from application.port.output.progress_output_port import (
    ProgressLifeCycleOutputPort,
)
from application.port.input.inferential_statistics_input_port import (
    InferentialStatisticsInputPort,
)
from typing import Generic, TypeVar

TOption = TypeVar("TOption")



class RunInferentialAnalysisUseCase(Generic[TOption],InferentialStatisticsInputPort[TOption]):
    def __init__(
        self,
        required: Set[Condition],
        subject_repo: SubjectRepository,
        collector: Collector,
        calculator: InferentialCalculator[TOption],
        post_processors: List[PostProcessor],
        progress_cycle_output_port: ProgressLifeCycleOutputPort,
        result_output_port: InferentialResultOutputPort,
    ):
        self.required = required
        self.subject_repo = subject_repo
        self.collector = collector
        self.calculator = calculator
        self.post_processors = post_processors
        self.progress_cycle_output_port = progress_cycle_output_port
        self.inferentional_result_output_port = result_output_port

    def execute(self,option:TOption) -> None:
        try:
            subjects = self._filter_subjects_by_conditions()
            grouped = self._collect(subjects)
            original = self._run_inferential_calculation(grouped,option)
            post_process_results = self._apply_post_processors(original)

            result = InferentialResultHistory(original, post_process_results)

            self.inferentional_result_output_port.present(subjects, result)
        except Exception as e:
            self.progress_cycle_output_port.on_error(e)
            raise

    def _filter_subjects_by_conditions(
        self,
    ) -> List[Subject]:
        self.progress_cycle_output_port.on_started(
            InferentialAnalysisStep.FILTER_SUBJECTS
        )
        subjects = [
            subject
            for subject in self.subject_repo.list_subjects()
            if subject.completed(self.required)
        ]
        self.progress_cycle_output_port.on_finished(
            InferentialAnalysisStep.FILTER_SUBJECTS
        )

        return subjects

    def _collect(
        self, subjects: List[Subject]
    ) -> GroupedValue:
        self.progress_cycle_output_port.on_started(
            InferentialAnalysisStep.COLLECT_VALUES
        )
        grouped = self.collector.collect(subjects,self.required)
        self.progress_cycle_output_port.on_finished(
            InferentialAnalysisStep.COLLECT_VALUES
        )
        return grouped

    def _run_inferential_calculation(self, grouped: GroupedValue,option:TOption) -> InferentialResult:
        self.progress_cycle_output_port.on_started(InferentialAnalysisStep.CALCULATE)
        original = self.calculator.calculate(grouped,option)
        self.progress_cycle_output_port.on_finished(InferentialAnalysisStep.CALCULATE)
        return original

    def _apply_post_processors(
        self, original: InferentialResult
    ) -> List[InferentialResult]:
        post_process_results: List[InferentialResult] = []

        self.progress_cycle_output_port.on_started(InferentialAnalysisStep.POST_PROCESS)
        for post_processor in self.post_processors:
            original = post_processor.process(original)
            post_process_results.append(original)
        self.progress_cycle_output_port.on_finished(
            InferentialAnalysisStep.POST_PROCESS
        )

        return post_process_results

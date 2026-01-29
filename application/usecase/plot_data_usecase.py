from typing import List, Dict
from application.model.graph_options import GraphOption
from application.port.output.graph_storage_output_port import GraphStorageOutputPort
from application.port.output.graph_generator import GraphGenerator
from application.model.graph_type import GraphType
from application.model.value_type import ValueType
from application.port.output.progress_output_port import ProgressLifeCycleOutputPort
from application.model.inferential_analysis_step import InferentialAnalysisStep
from application.service.collector.collector import Collector
from domain.value.grouped_value import GroupedValue
from domain.value.subject import Subject
from typing import Set
from domain.value.condition import Condition
from domain.repository.subject_repository import SubjectRepository
from application.service.collector.collector_factory import CollectorFactory
from application.port.input.plot_data_input_port import PlotDataInputPort


class PlotDataUseCase(PlotDataInputPort):
    """グラフ作成のユースケース"""

    def __init__(
        self,
        required: Set[Condition],
        subject_repo: SubjectRepository,
        collector: Collector,
        generator: GraphGenerator,
        progress_cycle_output_port: ProgressLifeCycleOutputPort,
        storage_output_port: GraphStorageOutputPort,
    ):
        self.required = required
        self.subject_repo = subject_repo
        self.collector = collector
        self.storage_output_port = storage_output_port
        self.progress_cycle_output_port = progress_cycle_output_port
        self.generator = generator

    def execute(
        self,
        graph_title: str,
        option: GraphOption,
    ):
        try:
            subjects = self._filter_subjects_by_conditions()
            grouped = self._collect(
                subjects,
            )
            self._save_fig(graph_title, grouped, option)
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

    def _collect(self, subjects: List[Subject]) -> GroupedValue:
        self.progress_cycle_output_port.on_started(
            InferentialAnalysisStep.COLLECT_VALUES
        )
        grouped = self.collector.collect(subjects, self.required)
        self.progress_cycle_output_port.on_finished(
            InferentialAnalysisStep.COLLECT_VALUES
        )
        return grouped

    def _save_fig(
        self,
        title: str,
        grouped: GroupedValue,
        option: GraphOption,
    ):
        # グラフ生成
        image_data = self.generator.generate(title, grouped, option=option)

        # 保存
        self.storage_output_port.save(title, image_data)

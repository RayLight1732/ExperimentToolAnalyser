from adapter.presenter.inferential_result_presenter import InferentialResultPresenter
from adapter.presenter.progress_presenter import ProgressPresenter
from application.model.graph_type import GraphType
from application.model.value_type import ValueType
from application.port.input.inferential_statistics_input_port import InferentialStatisticsInputPort
from application.port.output.graph_generator import GraphGenerator
from application.service.collector import collector_factory
from application.service.collector.collector_factory import CollectorFactory
from application.usecase.plot_data_usecase import PlotDataUseCase
from application.usecase.run_inferential_analysis_usecase import RunInferentialAnalysisUseCase
from bootstrap.context import AppContext
from domain.analysis.inferential.options.two_sample_test_option import TwoSampleTestOption
from domain.analysis.inferential.post_processor import PostProcessor
from domain.analysis.inferential.value_filter import ValueFilter
from domain.repository.inferential_result_repository import InferentialResultRepository
from domain.value.condition import Condition
from infra.calculator.inferential.calculator_factory import CalculatorFactory #TODO portにする
from typing import Dict, List, Set

from infra.strage.file_graph_storage import FileGraphStorage

class PlotDataUsecaseFactory:
    def __init__(self,context:AppContext,collector_factory:CollectorFactory,value_filters:List[ValueFilter],generators:List[GraphGenerator]):
        self.context = context
        self.value_filters = value_filters
        self.collector_factory = collector_factory
        self.generators: Dict[GraphType, GraphGenerator] = {
            gen.supported_type(): gen for gen in generators
        }

    def create_plot_usecase(
        self,
        value_type:ValueType,
        graph_type:GraphType,
        required:Set[Condition]
    ) -> PlotDataUseCase:
        progress_presenter = ProgressPresenter()
        storage_output_port = FileGraphStorage(self.context.config.save_dir)

        return PlotDataUseCase(
            required=required,
            subject_repo=self.context.subject_repository,
            collector=self.collector_factory.get(value_type),
            value_filters=self.value_filters,
            generator= self.generators[graph_type],
            progress_cycle_output_port=progress_presenter,
            storage_output_port=storage_output_port,
        )
from adapter.presenter.inferential_result_presenter import InferentialResultPresenter
from adapter.presenter.progress_presenter import ProgressPresenter
from application.model.value_type import ValueType
from application.port.input.inferential_statistics_input_port import InferentialStatisticsInputPort
from application.service.collector import collector_factory
from application.service.collector.collector_factory import CollectorFactory
from application.usecase.run_inferential_analysis_usecase import RunInferentialAnalysisUseCase
from bootstrap.context import AppContext
from domain.analysis.inferential.options.two_sample_test_option import TwoSampleTestOption
from domain.analysis.inferential.post_processor import PostProcessor
from domain.repository.inferential_result_repository import InferentialResultRepository
from domain.value.condition import Condition
from infra.calculator.inferential.calculator_factory import CalculatorFactory #TODO portにする
from typing import List, Set

class InferentialUsecaseFactory:
    def __init__(self,collector_factory:CollectorFactory,calculator_factory:CalculatorFactory):
        self.collector_factory = collector_factory
        self.calculator_factory = calculator_factory

    def create_wilcoxon_usecase(
        self,
        context:AppContext,
        post_processors:List[PostProcessor],
        value_type:ValueType,
        required:Set[Condition],
        file_name:str
    ) -> InferentialStatisticsInputPort[TwoSampleTestOption]:

        progress_presenter = ProgressPresenter()
        result_presenter = InferentialResultPresenter(
            file_name, context.inferential_result_repository
        )

        return RunInferentialAnalysisUseCase(
            required=required,
            subject_repo=context.subject_repository,
            collector=self.collector_factory.get(value_type),
            calculator=self.calculator_factory.create_wilcoxon_calculator(progress_presenter),
            post_processors=post_processors,
            progress_cycle_output_port=progress_presenter,
            result_output_port=result_presenter,
        )
from os import name
from application.model import value_type
from application.model.value_type import ValueType
from adapter.parser import comparison_from_json, test_args_from_json, two_sample_test_option_from_json
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
from bootstrap.context import AppContext
from bootstrap.inferential_statistics_factory import InferentialUsecaseFactory
from domain.analysis.inferential.options.two_sample_test_option import TwoSampleTestOption
from domain.analysis.inferential.test_type import TestType
from domain.repository.inferential_result_repository import InferentialResultRepository
from infra.post_processor.holm_post_processor import HolmPostProcessor


class InferentialStatisticsCLIController:
    def __init__(
        self,
        usecase_factory: InferentialUsecaseFactory # TODO I/Fにしたほうがいい
    ):
        self.usecase_factory = usecase_factory

    def handle(self, context:AppContext,input_line: str):
        test_type,value_type, required,file_name,option = test_args_from_json(input_line)
        post_processor = HolmPostProcessor()#TODO
        if test_type == TestType.WILCOXON_TEST:
            two_sample_test_option = two_sample_test_option_from_json(option)
            usecase = self.usecase_factory.create_wilcoxon_usecase(context,[post_processor],value_type,required,file_name)
            usecase.execute(two_sample_test_option)
        elif test_type == TestType.PAIRED_T_TEST:
            two_sample_test_option = two_sample_test_option_from_json(option)
            usecase = self.usecase_factory.create_paired_t_usecase(context,[post_processor],value_type,required,file_name)
            usecase.execute(two_sample_test_option)

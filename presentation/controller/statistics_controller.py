from typing import List, Optional
from application.port.input.statistics_orchestrator_input_port import (
    StatisticsOrchestratorInputPort,
)
from application.port.input.list_completed_subjects_input_port import (
    ListCompletedSubjectInputPort,
)
from domain.entity.subject import Subject
from application.dto.value_type import ValueType
from application.dto.filter_parameter import FilterParameter
from application.dto.mean_and_se import MeanAndSEByCondition
from application.port.input.save_calculation_result_input_port import (
    SaveCalculationResultInputPort,
)
from application.dto.t_test_result_dto import CorrectedAndOriginalValueByConditionPair


class StatisticsController:
    def __init__(
        self,
        list_completed_subjects_usecase: ListCompletedSubjectInputPort,
        mean_and_se_orchestrator: StatisticsOrchestratorInputPort,
        paired_t_test_orchestrator: StatisticsOrchestratorInputPort,
        save_calculation_result_input_port: SaveCalculationResultInputPort,
    ):
        self.mean_and_se_orchestrator = mean_and_se_orchestrator
        self.paired_t_test_orchestrator = paired_t_test_orchestrator
        self.list_completed_subjects_usecase = list_completed_subjects_usecase
        self.save_calculation_result_input_port = save_calculation_result_input_port

    def list_completed_subjects(self) -> List[Subject]:
        return self.list_completed_subjects_usecase.execute()

    def calculate_mean_and_se(
        self,
        value_types: List[ValueType],
        filter_parameter: Optional[FilterParameter] = None,
    ) -> None:
        self.mean_and_se_orchestrator.execute(value_types, filter_parameter)

    def run_paired_t_test_with_holm(
        self,
        value_types: List[ValueType],
        filter_parameter: Optional[FilterParameter] = None,
    ) -> None:
        self.paired_t_test_orchestrator.execute(value_types, filter_parameter)

    # def run_rm_anova(self, value_types: List[ValueType]) -> None:
    #     self.rm_anova_orchestrator.execute(value_types)

    def save_calculation_result(
        self,
        name: str,
        mean_and_se: MeanAndSEByCondition,
        t_test_result: CorrectedAndOriginalValueByConditionPair,
    ):
        self.save_calculation_result_input_port.execute(
            name, mean_and_se, t_test_result
        )

from typing import List
from application.port.input.statistics_orchestrator_input_port import (
    StatisticsOrchestratorInputPort,
)
from application.port.input.list_completed_subjects_input_port import (
    ListCompletedSubjectInputPort,
)
from domain.entity.subject import Subject
from application.dto.value_type import ValueType


class StatisticsController:
    def __init__(
        self,
        list_completed_subjects_usecase: ListCompletedSubjectInputPort,
        mean_and_se_orchestrator: StatisticsOrchestratorInputPort,
        paired_t_test_orchestrator: StatisticsOrchestratorInputPort,
    ):
        self.mean_and_se_orchestrator = mean_and_se_orchestrator
        self.paired_t_test_orchestrator = paired_t_test_orchestrator
        self.list_completed_subjects_usecase = list_completed_subjects_usecase

    def list_completed_subjects(self) -> List[Subject]:
        return self.list_completed_subjects_usecase.execute()

    def calculate_mean_and_se(self, value_types: List[ValueType]) -> None:
        self.mean_and_se_orchestrator.execute(value_types)

    def run_paired_t_test_with_holm(self, value_types: List[ValueType]) -> None:
        self.paired_t_test_orchestrator.execute(value_types)

    # def run_rm_anova(self, value_types: List[ValueType]) -> None:
    #     self.rm_anova_orchestrator.execute(value_types)

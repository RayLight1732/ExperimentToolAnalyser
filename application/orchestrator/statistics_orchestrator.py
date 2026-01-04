from application.port.input.statistics_orchestrator_input_port import (
    StatisticsOrchestratorInputPort,
)
from application.port.input.statistics_usecase_input_port import (
    StatisticsUsecaseInputPort,
)
from typing import List, Dict, Any
from application.dto.value_type import ValueType
from application.port.input.list_completed_subjects_input_port import (
    ListCompletedSubjectInputPort,
)
from application.port.input.collect_value_input_port import (
    CollectValueInputPort,
)


class StatisticsOrchestrator(StatisticsOrchestratorInputPort):

    def __init__(
        self,
        statistics_usecase: StatisticsUsecaseInputPort,
        list_completed_subjects_usecase: ListCompletedSubjectInputPort,
        collect_value_usecase: CollectValueInputPort,
    ):
        self.statistics_usecase = statistics_usecase
        self.list_completed_subjects_usecase = list_completed_subjects_usecase
        self.collect_value_usecase = collect_value_usecase

    def execute(
        self,
        value_types: List[ValueType],
    ) -> None:
        subjects = self.list_completed_subjects_usecase.execute()

        results: Dict[ValueType, Any] = {}
        for value_type in value_types:
            values = self.collect_value_usecase.execute(subjects, value_type)
            results[value_type] = self.statistics_usecase.execute(value_type, values)

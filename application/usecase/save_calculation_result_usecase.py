from application.dto.mean_and_se import (
    MeanAndSEByCondition,
    to_laveled_values as m_to_laveled_values,
)
from domain.repository.laveled_value_repository import LaveledValueRepository
from application.port.input.save_calculation_result_input_port import (
    SaveCalculationResultInputPort,
)
from application.dto.t_test_result_dto import (
    CorrectedAndOriginalValueByConditionPair,
    to_laveled_values as t_to_laveled_values,
)


class SaveCalculationResultUsecase(SaveCalculationResultInputPort):
    def __init__(self, repo: LaveledValueRepository) -> None:
        self.repo = repo

    def execute(
        self,
        name: str,
        mean_and_se: MeanAndSEByCondition,
        t_test_result: CorrectedAndOriginalValueByConditionPair,
    ):
        self.repo.save(
            name,
            [m_to_laveled_values(mean_and_se), t_to_laveled_values(t_test_result)],
        )

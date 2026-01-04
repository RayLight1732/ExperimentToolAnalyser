from application.dto.mean_and_se import MeanAndSEByCondition
from abc import ABC, abstractmethod
from application.dto.t_test_result_dto import CorrectedAndOriginalValueByConditionPair


class SaveCalculationResultInputPort(ABC):

    @abstractmethod
    def execute(
        self,
        name: str,
        mean_and_se: MeanAndSEByCondition,
        t_test_result: CorrectedAndOriginalValueByConditionPair,
    ):
        pass

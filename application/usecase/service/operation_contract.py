from enum import Enum
from typing import Dict
from domain.analysis.error.invaild_operation_error import InvalidOperationError


class ValueType(Enum):
    FMS = "fms"
    SSQ = "ssq"


class CalculationType(Enum):
    MEAN = "mean"
    MEAN_AND_SE = "mean_and_se"
    RM_ANOVA = "rm_anova"
    PAIRED_T_TEST_WITH_HOLM = "paired_t_test_with_holm"


class ValidOperations:
    def __init__(self, mapping: Dict[ValueType, set[CalculationType]]):
        self._mapping = mapping

    def ensure_valid(
        self,
        value_type: ValueType,
        calculation_type: CalculationType,
    ) -> None:
        if calculation_type not in self._mapping.get(value_type, set()):
            raise InvalidOperationError(
                f"{calculation_type} is not valid for {value_type}"
            )

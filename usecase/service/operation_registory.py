from domain.service.collector import Collector
from domain.service.calculator import Calculator
from domain.analysis.operation import Operation
from typing import Dict, Any, List
from dataclasses import dataclass
from enum import Enum
from bootstrap.config import Config


class ValueType(Enum):
    FMS = "fms"
    SSQ = "ssq"


class CalculationType(Enum):
    MEAN = "mean"
    MEAN_AND_SE = "mean_and_se"
    RM_ANOVA = "rm_anova"


@dataclass(frozen=True)
class ValidOperations:
    value: Dict[ValueType, List[CalculationType]]


class OperationRegistory:
    def __init__(
        self,
        valid_operations: ValidOperations,
        collectors: Dict[ValueType, Collector],
        calculators: Dict[CalculationType, Calculator[Any]],
    ):
        self.valid_operations = valid_operations
        self.collectors = collectors
        self.calculators = calculators

    def get_operation(
        self, value_type: ValueType, calculation_type: CalculationType
    ) -> Operation[Any]:

        operations = ValidOperations.value.get(value_type)
        if operations is None:
            raise ValueError("Invalid operation : value type")
        if calculation_type not in operations:
            raise ValueError("Invalid operation : calculation type")

        collector = self.collectors.get(value_type)
        calculator = self.calculators.get(calculation_type)

        if collector is None or calculator is None:
            raise ValueError("Collector or Calculator not found")

        return Operation(collector, calculator)


def new_operation_registory(
    config: Config,
    collectors: Dict[ValueType, Collector],
    calculators: Dict[CalculationType, Calculator[Any]],
) -> OperationRegistory:

    return OperationRegistory(config.valid_operations, collectors, calculators)

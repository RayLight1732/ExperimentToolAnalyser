from domain.service.collector import Collector
from domain.service.calculator import Calculator
from domain.analysis.operation import Operation
from typing import Dict, Any
from bootstrap.config import Config
from usecase.service.operation_contract import (
    ValueType,
    CalculationType,
    ValidOperations,
)


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

        self.valid_operations.ensure_valid(value_type, calculation_type)

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

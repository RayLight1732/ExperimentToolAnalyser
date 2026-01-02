import math
from typing import Dict
from domain.value_object.condition import Condition
from domain.value_object.grouped_value import GroupedValue
from domain.service.calculator import Calculator
from domain.analysis.result.mean_and_se import MeanAndSEByCondition, MeanAndSE


class MeanAndSECalculator(Calculator[float, MeanAndSEByCondition]):

    def calculate(self, collected: GroupedValue[float]) -> MeanAndSEByCondition:

        result: Dict[Condition, MeanAndSE] = {}

        for condition, subject_values in collected.value.items():
            values = list(subject_values.values())

            if len(values) == 0:
                raise ValueError(f"No data for condition: {condition}")

            n = len(values)
            mean = sum(values) / n

            if n == 1:
                # 標準誤差は定義できないが、Domain判断として 0.0 にする例
                se = 0.0
            else:
                variance = sum((v - mean) ** 2 for v in values) / (n - 1)
                std_dev = math.sqrt(variance)
                se = std_dev / math.sqrt(n)

            result[condition] = MeanAndSE.from_float(mean, se)

        return MeanAndSEByCondition(result)

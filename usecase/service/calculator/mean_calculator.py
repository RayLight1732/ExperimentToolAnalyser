from domain.service.calculator import Calculator
from domain.value_object.grouped_value import GroupedValue
from domain.value_object.condition import Condition
from typing import Dict
from collections import defaultdict
from domain.analysis.result.mean_and_se import MeanByCondition


class MeanCalculator(Calculator[MeanByCondition]):
    def calculate(self, collected: GroupedValue[float]) -> MeanByCondition:
        condition_value_dict: Dict[Condition, float] = defaultdict(lambda: 0)
        for condition, subject_data_map in collected.value.items():
            condition_value_dict[condition] = sum(subject_data_map.values()) / len(
                subject_data_map
            )

        return MeanByCondition(dict(condition_value_dict))

import math
from typing import Dict, List
from domain.analysis.descriptive.descriptive_calculator import DescriptiveCalculator
from domain.value.condition import Condition
from domain.value.grouped_value import GroupedValue
from domain.analysis.descriptive.result.descriptive_result import DescriptiveResult
from domain.analysis.descriptive.result.metric_type import MetricType
from domain.analysis.descriptive.result.metric import Metric
from collections import defaultdict


class MeanCalculator(DescriptiveCalculator):

    def __init__(self):
        pass

    def calculate(self, grouped: GroupedValue) -> DescriptiveResult:

        result: Dict[Condition, List[Metric]] = defaultdict(lambda: [])

        for condition, subject_values in grouped.value.items():
            values = list(subject_values.values())

            n = len(values)
            mean = sum(values) / n

            result[condition].append(Metric(MetricType.MEAN, mean))

        return DescriptiveResult(dict(result))

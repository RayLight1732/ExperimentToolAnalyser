import math
from typing import Dict,List
from domain.statistics.descriptive.descriptive_calculator import DescriptiveCalculator
from domain.value.condition import Condition
from domain.value.grouped_value import GroupedValue
from domain.statistics.descriptive.result.descriptive_result import DescriptiveResult
from domain.statistics.descriptive.result.metric_type import MetricType
from domain.statistics.descriptive.result.metric import Metric

class MeanCalculator(DescriptiveCalculator):

    def __init__(self):
        pass

    def calculate(
        self,
        grouped: GroupedValue
    ) -> DescriptiveResult:

        result: Dict[Condition,List[Metric]] = {}

        for condition, subject_values in grouped.value.items():
            values = list(subject_values.values())

            n = len(values)
            mean = sum(values) / n

            result[condition] = Metric(MetricType.MEAN,mean)

        return DescriptiveResult(result)

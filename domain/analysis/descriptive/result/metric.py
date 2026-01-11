from dataclasses import dataclass

from domain.analysis.descriptive.result.metric_type import MetricType


@dataclass(frozen=True)
class Metric:
    type: MetricType
    value: float

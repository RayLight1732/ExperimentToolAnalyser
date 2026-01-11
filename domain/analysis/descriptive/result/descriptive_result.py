from dataclasses import dataclass
from domain.analysis.descriptive.result.metric import Metric
from domain.value.condition import Condition
from typing import List, Dict


@dataclass(frozen=True)
class DescriptiveResult:
    values: Dict[Condition, List[Metric]]

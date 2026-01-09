from dataclasses import dataclass
from typing import List

from domain.statistics.inferential.result.statistical_result import StatisticalResult

@dataclass(frozen=True)
class StatisticalResultHistory:
    original:StatisticalResult
    post_process:List[StatisticalResult]
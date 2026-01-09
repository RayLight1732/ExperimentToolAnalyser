from dataclasses import dataclass
from typing import Dict
from domain.statistics.inferential.result.comparition import Comparison
from domain.statistics.inferential.result.evidence import Evidence

@dataclass(frozen=True)
class StatisticalResult:
    method: str
    comparisons: Dict[Comparison,Evidence]
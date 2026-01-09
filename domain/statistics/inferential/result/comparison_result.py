from dataclasses import dataclass

from domain.statistics.inferential.result.comparition import Comparison
from domain.statistics.inferential.result.evidence import Evidence

@dataclass(frozen=True)
class ComparisonResult:
    comparison: Comparison
    evidence: Evidence
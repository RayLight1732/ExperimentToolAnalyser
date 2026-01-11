from dataclasses import dataclass
from typing import Dict
from domain.analysis.inferential.result.comparison import Comparison
from domain.analysis.inferential.result.evidence import Evidence


@dataclass(frozen=True)
class InferentialResult:
    method: str
    comparisons: Dict[Comparison, Evidence]

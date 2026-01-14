from dataclasses import dataclass
from application.dto.inferential_analysis_step import InferentialAnalysisStep


@dataclass(frozen=True)
class ProgressPhase:
    name: str
    category: InferentialAnalysisStep

    def __str__(self) -> str:
        return f"{self.category}:{self.name}"

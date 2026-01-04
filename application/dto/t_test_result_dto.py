from dataclasses import dataclass
from typing import Self
from domain.analysis.result.by_condition_pair import ByConditionPair


@dataclass(frozen=True)
class CorrectedAndOriginalValue:
    @classmethod
    def from_float(
        cls,
        original: float,
        corrected: float,
    ) -> Self:
        return cls(corrected, original)

    corrected: float
    original: float


CorrectedAndOriginalValueByConditionPair = ByConditionPair[CorrectedAndOriginalValue]

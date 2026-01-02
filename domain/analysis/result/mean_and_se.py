from dataclasses import dataclass
from typing import Self
from domain.analysis.result.by_condition import ByCondition

@dataclass(frozen=True)
class MeanAndSE:
    @classmethod
    def from_float(cls,mean:float,standard_error:float)->Self:
        return cls(mean,standard_error)
    mean:float
    standard_error:float

MeanAndSEByCondition = ByCondition[MeanAndSE]
MeanByCondition = ByCondition[float]

from dataclasses import dataclass
from typing import Self
from domain.analysis.result.by_condition import ByCondition
from domain.value_object.laveled_value import LaveledValues, LaveledValue


@dataclass(frozen=True)
class MeanAndSE:
    @classmethod
    def from_float(cls, mean: float, standard_error: float) -> Self:
        return cls(mean, standard_error)

    mean: float
    standard_error: float


MeanAndSEByCondition = ByCondition[MeanAndSE]
MeanByCondition = ByCondition[float]


def to_laveled_values(value: MeanAndSEByCondition) -> LaveledValues:
    condition_list = []
    mean_list = []
    se_list = []
    for condition, mean_and_se in sorted(
        value.values.items(),
        key=lambda item: str(item[0]),
    ):
        condition_list.append(str(condition))
        mean_list.append(mean_and_se.mean)
        se_list.append(mean_and_se.standard_error)

    return LaveledValues(
        [
            LaveledValue("条件", condition_list),
            LaveledValue("平均値", mean_list),
            LaveledValue("標準誤差", se_list),
        ]
    )

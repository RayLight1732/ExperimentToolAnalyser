from dataclasses import dataclass
from typing import Self
from domain.analysis.result.by_condition_pair import ByConditionPair
from domain.value_object.laveled_value import LaveledValues, LaveledValue


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


def to_laveled_values(value: CorrectedAndOriginalValueByConditionPair) -> LaveledValues:
    condition_list_0 = []
    condition_list_1 = []
    original_list = []
    corrected_list = []
    for condition, result in sorted(
        value.values.items(),
        key=lambda item: str(item[0]),
    ):
        condition_list_0.append(str(condition[0]))
        condition_list_1.append(str(condition[1]))
        original_list.append(result.original)
        corrected_list.append(result.corrected)

    return LaveledValues(
        [
            LaveledValue("条件1", condition_list_0),
            LaveledValue("条件2", condition_list_1),
            LaveledValue("元の値", original_list),
            LaveledValue("Holm補正後", corrected_list),
        ]
    )

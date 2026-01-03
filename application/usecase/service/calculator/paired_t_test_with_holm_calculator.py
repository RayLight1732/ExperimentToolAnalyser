from domain.service.calculator import Calculator
from domain.analysis.result.by_condition_pair import ByConditionPair
from domain.value_object.grouped_value import GroupedValue
from domain.value_object.condition import Condition
from typing import Tuple, Self
from itertools import combinations
from scipy.stats import ttest_rel
from statsmodels.stats.multitest import multipletests  # type: ignore[import-untyped]
import numpy as np
from dataclasses import dataclass


@dataclass(frozen=True)
class CorrectedAndOriginalValue:
    @classmethod
    def from_float(cls, corrected: float, original: float) -> Self:
        return cls(corrected, original)

    corrected: float
    original: float


CorrectedAndOriginalValueByConditionPair = ByConditionPair[CorrectedAndOriginalValue]


class PairedTTestWithHolmCalculator(
    Calculator[CorrectedAndOriginalValueByConditionPair]
):
    """
    GroupedValue[float] を受け取り、
    条件間の対応のある t 検定を行い、
    Holm 法で補正した p 値を返す Calculator
    """

    def calculate(
        self, collected: GroupedValue[float]
    ) -> CorrectedAndOriginalValueByConditionPair:

        conditions = list(collected.value.keys())

        raw_pvalues: list[float] = []
        pairs: list[Tuple[Condition, Condition]] = []

        # 条件ペアごとに対応のある t 検定
        for c1, c2 in combinations(conditions, 2):
            data1 = collected.value[c1]
            data2 = collected.value[c2]

            # 共通被験者のみ抽出
            common_subjects = set(data1.keys()) & set(data2.keys())

            if len(common_subjects) < 2:
                # 対応ありt検定ができない場合はスキップ or 例外
                continue

            v1 = np.array([data1[s] for s in common_subjects])
            v2 = np.array([data2[s] for s in common_subjects])

            _, p = ttest_rel(v1, v2)

            assert isinstance(p, float)
            raw_pvalues.append(p)
            pairs.append((c1, c2))

        if not raw_pvalues:
            return CorrectedAndOriginalValueByConditionPair({})
        # Holm 法による補正
        _, corrected_pvalues, _, _ = multipletests(  # type: ignore
            raw_pvalues, alpha=0.05, method="holm"
        )

        return CorrectedAndOriginalValueByConditionPair(
            {
                pair: CorrectedAndOriginalValue.from_float(float(p[0]), float(p[1]))
                for pair, p in zip(pairs, zip(raw_pvalues, corrected_pvalues))  # type: ignore
            }
        )

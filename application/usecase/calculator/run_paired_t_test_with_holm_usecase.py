from domain.value_object.condition import Condition
from domain.value_object.grouped_value import GroupedValue
from application.port.input.statistics_usecase_input_port import (
    StatisticsUsecaseInputPort,
)
from application.port.output.calculator.run_paired_t_test_with_holm_output_port import (
    RunPairedTTestWithHolmOutputPort,
)
from domain.value_object.condition import Condition
from typing import Tuple
from itertools import combinations
from scipy.stats import ttest_rel
from statsmodels.stats.multitest import multipletests  # type: ignore[import-untyped]
import numpy as np
from application.dto.t_test_result_dto import (
    CorrectedAndOriginalValue,
    CorrectedAndOriginalValueByConditionPair,
)
from application.dto.value_type import ValueType


class RunPairedTTestWithHolmUsecase(StatisticsUsecaseInputPort):

    def __init__(self, output_port: RunPairedTTestWithHolmOutputPort):
        self.output_port = output_port

    def execute(
        self,
        value_type: ValueType,
        values: GroupedValue,
    ) -> None:
        self.output_port.on_start(value_type)
        result = self._calculate(values)
        self.output_port.on_complete(value_type, result)

    def _calculate(
        self, collected: GroupedValue
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

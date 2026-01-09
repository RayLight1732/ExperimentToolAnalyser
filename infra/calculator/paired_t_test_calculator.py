from typing import List
from itertools import combinations
from scipy.stats import ttest_rel
import numpy as np

from application.port.output.progress_output_port import ProgressAdvanceOutputPort
from domain.statistics.inferential.result.comparition import Comparison
from domain.statistics.inferential.result.evidence import Evidence
from domain.statistics.inferential.result.statistical_result import StatisticalResult
from domain.statistics.inferential.inferential_calculator import InferentialCalculator
from domain.statistics.inferential.result.comparison_result import ComparisonResult
from domain.value.grouped_value import GroupedValue

class PairedTTestCalculator(InferentialCalculator):
    METHOD = "paired_t"

    def __init__(self, output_port: ProgressAdvanceOutputPort):
        self.output_port = output_port

    def calculate(
        self,
        grouped: GroupedValue
    ) -> StatisticalResult:
        conditions = list(grouped.value.keys())

        result:List[ComparisonResult] = []

        # 条件ペアごとに対応のある t 検定
        for c1, c2 in combinations(conditions, 2):
            data1 = grouped.value[c1]
            data2 = grouped.value[c2]

            # 共通被験者のみ抽出
            common_subjects = set(data1.keys()) & set(data2.keys())

            if len(common_subjects) < 2:
                # 対応ありt検定ができない場合はスキップ or 例外
                continue

            v1 = np.array([data1[s] for s in common_subjects])
            v2 = np.array([data2[s] for s in common_subjects])

            _, p = ttest_rel(v1, v2)

            assert isinstance(p, float)

            result.append(ComparisonResult(Comparison(v1,v2),Evidence(p_value=p)))

        return StatisticalResult(method=PairedTTestCalculator.METHOD,comparisons=result)


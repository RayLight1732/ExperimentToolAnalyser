from typing import Any, Dict, Set
from itertools import combinations
from scipy.stats import wilcoxon
import numpy as np

from application.port.output.progress_output_port import ProgressAdvanceOutputPort
from domain.analysis.inferential.options.two_sample_test_option import TwoSampleTestOption
from domain.analysis.inferential.result.comparison import Comparison
from domain.analysis.inferential.result.evidence import Evidence
from domain.analysis.inferential.result.inferential_result import InferentialResult
from domain.analysis.inferential.inferential_calculator import InferentialCalculator
from domain.analysis.inferential.test_type import TestType
from domain.value.grouped_value import GroupedValue
from domain.value.condition import Condition

class WilcoxonCalculator(InferentialCalculator[TwoSampleTestOption]):
    def __init__(self, output_port: ProgressAdvanceOutputPort):
        self.output_port = output_port

    def calculate(self, grouped: GroupedValue,option:TwoSampleTestOption) -> InferentialResult:
        
        conditions = list(grouped.value.keys())

        result: Dict[Comparison, Evidence] = {}

        # 条件ペアごとに対応のある t 検定
        for c1, c2 in pairs:
            data1 = grouped.value[c1]
            data2 = grouped.value[c2]

            # 共通被験者のみ抽出
            common_subjects = set(data1.keys()) & set(data2.keys())

            if len(common_subjects) < 2:
                # 対応ありt検定ができない場合はスキップ or 例外
                continue

            v1 = np.array([data1[s] for s in common_subjects])
            v2 = np.array([data2[s] for s in common_subjects])

            _, p = wilcoxon(v1, v2, alternative="two-sided")

            assert isinstance(p, float)

            result[Comparison(c1, c2)] = Evidence(p_value=p)

        return InferentialResult(method=TestType.WILCOXON_TEST, comparisons=result)

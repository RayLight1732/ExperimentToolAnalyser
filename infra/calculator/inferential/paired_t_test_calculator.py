from typing import Dict,Set
from itertools import combinations
from scipy.stats import ttest_rel
import numpy as np
from statsmodels.stats.power import TTestPower
from application.port.output.progress_output_port import ProgressAdvanceOutputPort
from domain.analysis.inferential.options.two_sample_test_option import TwoSampleTestOption
from domain.analysis.inferential.result.comparison import Comparison
from domain.analysis.inferential.result.evidence import Evidence
from domain.analysis.inferential.result.inferential_result import InferentialResult
from domain.analysis.inferential.inferential_calculator import InferentialCalculator
from domain.analysis.inferential.test_type import TestType
from domain.value.condition import CoolingMode, Position
from domain.value.grouped_value import GroupedValue

class PairedTTestCalculator(InferentialCalculator[TwoSampleTestOption]):

    def __init__(self, output_port: ProgressAdvanceOutputPort):
        self.output_port = output_port

    def calculate(self, grouped: GroupedValue,option:TwoSampleTestOption) -> InferentialResult:

        if len(option.comparisons) == 0:
            conditions = list(grouped.value.keys())
            pairs = combinations(conditions,2)
        else:
            pairs = [(comparison.left,comparison.right) for comparison in option.comparisons]

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

            _, p = ttest_rel(v1, v2)

            diff = v1 - v2
            sd = diff.std(ddof=1)

            required_n_80 = None
            if sd > 0:
                effect_size = diff.mean() / sd

                # 効果量が0でなければ必要人数を計算
                if effect_size != 0:
                    m_map = {
                        (CoolingMode.PERIODIC,CoolingMode.ALWAYS):10,
                        (CoolingMode.SICK_SCENE_ONLY,CoolingMode.ALWAYS):9,
                        (CoolingMode.ALWAYS_STRONG,CoolingMode.ALWAYS):8,
                        (CoolingMode.NONE,CoolingMode.SICK_SCENE_ONLY):7,
                        (CoolingMode.NONE,CoolingMode.SICK_SCENE_ONLY):6,
                        (CoolingMode.PERIODIC,CoolingMode.NONE):5,
                        (CoolingMode.ALWAYS_STRONG,CoolingMode.NONE):4,
                    }
                    m = m_map.get((c1.mode,c2.mode),None)
                    m = m if m is not None else m_map.get((c2.mode,c1.mode),None)

                    if m is not None:
                        alpha_eff = 0.05 / m

                        required_n_80 = TTestPower().solve_power(
                            effect_size=abs(effect_size),
                            alpha=alpha_eff,
                            power=0.8,
                            alternative="two-sided"
                        )
                        print("power",c1.mode.display_name,c2.mode.display_name,required_n_80)

            assert isinstance(p, float)

            result[Comparison(c1, c2)] = Evidence(p_value=p)

        return InferentialResult(
            method=TestType.PAIRED_T_TEST.name, comparisons=result
        )

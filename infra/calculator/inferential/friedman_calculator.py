from typing import Dict, List, Any
from domain.analysis.inferential.result.comparison import Comparison
from domain.analysis.inferential.result.evidence import Evidence
from domain.analysis.inferential.inferential_calculator import InferentialCalculator
from domain.analysis.inferential.result.inferential_result import InferentialResult
from domain.value.grouped_value import GroupedValue
from statsmodels.stats.anova import AnovaRM, AnovaResults  # type: ignore[import-untyped]
import pandas as pd
from application.port.output.progress_output_port import ProgressAdvanceOutputPort
from typing import cast
from scipy.stats import friedmanchisquare


class FriedmanCalculator(InferentialCalculator):
    METHOD = "friedman"

    def __init__(self, output_port: ProgressAdvanceOutputPort):
        self.output_port = output_port

    def calculate(self, grouped: GroupedValue) -> InferentialResult:
        df = self._to_long_dataframe(grouped)
        pivot = df.pivot(index="subject", columns="condition", values="value")

        stat, p = friedmanchisquare(
            *[pivot[c].to_numpy(dtype=float) for c in pivot.columns]
        )
        evidence = Evidence(p_value=float(p))
        return InferentialResult(self.METHOD, {Comparison.global_(): evidence})

    def _to_long_dataframe(self, data: GroupedValue) -> pd.DataFrame:
        records: List[Dict[str, Any]] = []
        for condition, subject_values in data.value.items():
            for subject, value in subject_values.items():
                records.append(
                    {
                        "subject": subject.name,
                        "condition": condition,
                        "value": value,
                    }
                )
        return pd.DataFrame.from_records(records)

from typing import Dict, List, Any
from domain.analysis.inferential.result.comparison import Comparison
from domain.analysis.inferential.result.evidence import Evidence
from domain.analysis.inferential.inferential_calculator import InferentialCalculator
from domain.analysis.inferential.result.inferential_result import InferentialResult
from domain.value.grouped_value import GroupedValue
from domain.value.condition import Condition
import pandas as pd
from application.port.output.progress_output_port import ProgressAdvanceOutputPort
from typing import Set
from scipy.stats import friedmanchisquare


class FriedmanCalculator(InferentialCalculator):
    METHOD = "friedman"

    def __init__(self, output_port: ProgressAdvanceOutputPort):
        self.output_port = output_port

    def calculate(self, grouped: GroupedValue,target:Set[Condition]) -> InferentialResult:
        df = self._to_long_dataframe(grouped,target)
        pivot = df.pivot(index="subject", columns="condition", values="value")

        stat, p = friedmanchisquare(
            *[pivot[c].to_numpy(dtype=float) for c in pivot.columns]
        )
        evidence = Evidence(p_value=float(p))
        return InferentialResult(self.METHOD, {Comparison.global_(): evidence})

    def _to_long_dataframe(self, data: GroupedValue,target:Set[Condition]) -> pd.DataFrame:
        records: List[Dict[str, Any]] = []
        for condition, subject_values in data.value.items():
            if not condition in target:
                continue
            for subject, value in subject_values.items():
                records.append(
                    {
                        "subject": subject.name,
                        "condition": condition,
                        "value": value,
                    }
                )
        return pd.DataFrame.from_records(records)

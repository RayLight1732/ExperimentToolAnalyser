from typing import Dict, List, Any
from domain.analysis.inferential.result.comparison import Comparison
from domain.analysis.inferential.result.evidence import Evidence
from domain.analysis.inferential.inferential_calculator import InferentialCalculator
from domain.analysis.inferential.result.inferential_result import InferentialResult
from domain.value.grouped_value import GroupedValue
from statsmodels.stats.anova import AnovaRM, AnovaResults  # type: ignore[import-untyped]
import pandas as pd
from application.port.output.progress_output_port import ProgressAdvanceOutputPort


class RMAnovaCalculator(InferentialCalculator):
    METHOD = "rm_anova"

    def __init__(self, output_port: ProgressAdvanceOutputPort):
        self.output_port = output_port

    def calculate(self, grouped: GroupedValue) -> InferentialResult:
        df = self._to_long_dataframe(grouped)

        anova = AnovaRM(
            data=df, depvar="value", subject="subject", within=["condition"]
        )

        anova_results = anova.fit()
        evidence = Evidence(p_value=anova_results.anova_table["p"])  # type: ignore TODO
        return InferentialResult(
            RMAnovaCalculator.METHOD, {Comparison.global_(): evidence}
        )

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

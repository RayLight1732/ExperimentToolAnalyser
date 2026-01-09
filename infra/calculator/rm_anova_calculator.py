from typing import Dict,List, Any
from domain.statistics.inferential.result.comparition import Comparison
from domain.statistics.inferential.result.evidence import Evidence
from domain.statistics.inferential.inferential_calculator import InferentialCalculator
from domain.statistics.inferential.result.statistical_result import StatisticalResult
from domain.value.grouped_value import GroupedValue
from statsmodels.stats.anova import AnovaRM, AnovaResults  # type: ignore[import-untyped]
import pandas as pd
from application.port.output.progress_output_port import ProgressAdvanceOutputPort

class RMAnovaCalculator(InferentialCalculator):
    METHOD = "rm_anova"
    def __init__(self,  output_port: ProgressAdvanceOutputPort):
        self.output_port = output_port

    def calculate(
        self,
        grouped: GroupedValue
    ) -> StatisticalResult:
        df = self._to_long_dataframe(grouped
                                     )

        anova = AnovaRM(
            data=df, depvar="value", subject="subject", within=["condition"]
        )

        anova_results = anova.fit()
        evidence = Evidence(p_value=anova_results.anova_table["p"])
        return StatisticalResult(RMAnovaCalculator.METHOD,{Comparison.global_(),evidence})

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


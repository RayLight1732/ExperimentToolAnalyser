from typing import Dict
from domain.value_object.grouped_value import GroupedValue
from application.port.input.statistics_usecase_input_port import (
    StatisticsUsecaseInputPort,
)
from application.port.output.calculator.run_rm_anova_output_port import (
    RunRMAnovaOutputPort,
)
from typing import List, Any
from statsmodels.stats.anova import AnovaRM, AnovaResults  # type: ignore[import-untyped]
import pandas as pd
from application.dto.rm_anova_result_dto import RMAnovaResult
from application.dto.value_type import ValueType


class RunRMAnovaUsecase(StatisticsUsecaseInputPort):

    def __init__(self, output_port: RunRMAnovaOutputPort):
        self.output_port = output_port

    def execute(
        self,
        value_type: ValueType,
        values: GroupedValue[float],
    ) -> None:
        self.output_port.on_start(value_type)
        result = self._calculate(values)
        self.output_port.on_complete(value_type, self._to_rm_anova_result_dto(result))

    def _calculate(self, collected: GroupedValue[float]) -> AnovaResults:
        df = self._to_long_dataframe(collected)

        anova = AnovaRM(
            data=df, depvar="value", subject="subject", within=["condition"]
        )

        return anova.fit()

    def _to_long_dataframe(self, data: GroupedValue[float]) -> pd.DataFrame:
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

    def _to_rm_anova_result_dto(self, anova_results: AnovaResults) -> RMAnovaResult:
        return RMAnovaResult(anova_table=anova_results.anova_table)

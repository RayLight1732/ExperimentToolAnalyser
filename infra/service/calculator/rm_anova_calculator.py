from statsmodels.stats.anova import AnovaRM,AnovaResults # type: ignore[import-untyped]

from domain.service.calculator import Calculator
from usecase.grouped_value import GroupedValue
import pandas as pd


#TODO 専用のoutputを作る
class RMAnovaCalculator(Calculator[float, AnovaResults]):
    def calculate(self, collected: GroupedValue[float]) -> AnovaResults:
        df = self._to_long_dataframe(collected)

        anova = AnovaRM(
            data=df,
            depvar="value",
            subject="subject",
            within=["condition"]
        )

        #TODO
        return anova.fit()

    def _to_long_dataframe(self,data: GroupedValue[float]) -> pd.DataFrame:
        records = []
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

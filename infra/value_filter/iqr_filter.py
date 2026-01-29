from ast import Dict
from typing import Set
from domain.analysis.inferential.value_filter import ValueFilter
import numpy as np

from domain.value.condition import Condition
from domain.value.grouped_value import GroupedValue
from domain.value.subject_data import SubjectData

class IQRFilter(ValueFilter):
    def __init__(self,iqr_factor:float = 1.5):
        self.iqr_factor = iqr_factor

    def apply(self, grouped:GroupedValue):
        outlier_subjects: Set[SubjectData] = set()

        # ① 条件ごとに外れ値判定
        for condition, subject_values in grouped.value.items():
            vals = np.array(list(subject_values.values()))

            q1 = np.percentile(vals, 25)
            q3 = np.percentile(vals, 75)
            iqr = q3 - q1

            lower = q1 - self.iqr_factor * iqr
            upper = q3 + self.iqr_factor * iqr

            for subject, v in subject_values.items():
                if v < lower or v > upper:
                    outlier_subjects.add(subject)

        # ② 外れ値を出した被験者を全条件から除外
        cleaned: Dict[Condition, Dict[SubjectData, float]] = {}

        for condition, subject_values in grouped.value.items():
            cleaned[condition] = {
                subject: v
                for subject, v in subject_values.items()
                if subject not in outlier_subjects
            }

        return GroupedValue(grouped.name,cleaned)

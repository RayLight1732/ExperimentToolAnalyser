from ast import Dict
from typing import List, Set
from domain.analysis.inferential.value_filter import ValueFilter
import numpy as np

from domain.value.condition import Condition
from domain.value.grouped_value import GroupedValue
from domain.value.subject_data import SubjectData

class NameFilter(ValueFilter):
    def __init__(self,sensored:List[str]):
        self.sensored = sensored

    def apply(self, grouped:GroupedValue):
        result = {}
        print("start name filter")
        for condition,subject_values in grouped.value.items():
            new_subject_values = {}
            for subject_data,value in subject_values.items():
                if not subject_data.name in self.sensored:
                    new_subject_values[subject_data] = value
            result[condition] = new_subject_values
        print("end name filter")

        return GroupedValue(grouped.name,result)

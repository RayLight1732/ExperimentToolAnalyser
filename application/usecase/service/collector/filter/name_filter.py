from application.usecase.service.collector.filter.filter import Filter
from domain.value_object.grouped_value import GroupedValue
from typing import Any


class NameFilter(Filter):
    def __init__(self) -> None:
        super().__init__()

    def filter(self, values: GroupedValue[float], param: Any) -> GroupedValue[float]:
        if isinstance(param, list):
            raise ValueError("param must be List[str]")

        result = {}
        for condition, subject_value_map in values.value.items():
            new_subject_value_map = {}
            for subject, value in subject_value_map.items():
                if not subject.name in param:
                    new_subject_value_map[subject] = value
            result[condition] = new_subject_value_map

        return GroupedValue(result)

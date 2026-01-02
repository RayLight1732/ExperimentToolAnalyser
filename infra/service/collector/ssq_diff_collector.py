from domain.service.collector import Collector
from domain.entity.subject import Subject
from domain.value_object.subject_data import SubjectData
from domain.value_object.grouped_value import GroupedValue
from domain.value_object.condition import Condition
from domain.repository.ssq_repository import SSQRepository
from domain.value_object.time_point import TimePoint
from domain.value_object.ssq import SSQValueType
from typing import List, Dict
from collections import defaultdict


class SSQDiffCollector(Collector[float]):
    def __init__(self, ssq_repo: SSQRepository, value_type: SSQValueType):
        super().__init__()
        self.ssq_repo = ssq_repo
        self.value_type = value_type

    def collect(self, subjects: List[Subject]) -> GroupedValue[float]:
        result: Dict[Condition, Dict[SubjectData, float]] = defaultdict(lambda: dict())
        for subject in subjects:
            for session in subject.sessions:
                ssq_before = self.ssq_repo.get_ssq(
                    subject.data.name,
                    session.condition,
                    TimePoint.BEFORE,
                    session.result.ssq_timestamp[TimePoint.BEFORE],
                )
                ssq_after = self.ssq_repo.get_ssq(
                    subject.data.name,
                    session.condition,
                    TimePoint.AFTER,
                    session.result.ssq_timestamp[TimePoint.AFTER],
                )
                result[session.condition][subject.data] = ssq_after.get_value(
                    self.value_type
                ) - ssq_before.get_value(self.value_type)

        return GroupedValue(dict(result))

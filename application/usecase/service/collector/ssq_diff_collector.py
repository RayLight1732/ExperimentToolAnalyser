from application.usecase.service.collector.collector import Collector
from domain.entity.subject import Subject
from domain.value_object.subject_data import SubjectData
from domain.value_object.grouped_value import GroupedValue
from domain.value_object.condition import Condition
from domain.repository.ssq_repository import SSQRepository
from domain.value_object.time_point import TimePoint
from domain.value_object.ssq import SSQValueType
from typing import List, Dict
from collections import defaultdict
from application.port.output.collect_value_output_port import CollectValueOutputPort
from application.dto.value_type import ValueType


class SSQDiffCollector(Collector):
    def __init__(
        self,
        ssq_repo: SSQRepository,
        value_type: SSQValueType,
        output_port: CollectValueOutputPort,
    ):
        super().__init__()
        self.ssq_repo = ssq_repo
        self.value_type = value_type
        self.output_port = output_port

    def collect(self, subjects: List[Subject]) -> GroupedValue:
        self.output_port.on_start(ValueType.from_ssq_value_type(self.value_type))
        result: Dict[Condition, Dict[SubjectData, float]] = defaultdict(lambda: dict())

        length = sum(len(subject.sessions) for subject in subjects)
        count = 0

        try:
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

                    count += 1
                    self.output_port.on_progress(
                        ValueType.from_ssq_value_type(self.value_type),
                        count,
                        length,
                    )
        except Exception as e:
            self.output_port.on_error(ValueType.from_ssq_value_type(self.value_type), e)

        grouped = GroupedValue(f"ssq_diff_{self.value_type}", dict(result))
        self.output_port.on_complete(
            ValueType.from_ssq_value_type(self.value_type), grouped
        )
        return grouped

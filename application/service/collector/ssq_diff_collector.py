from application.dto.progress_phase import ProgressPhase
from application.service.collector.collector import Collector
from domain.value.subject import Subject
from domain.value.subject_data import SubjectData
from domain.value.grouped_value import GroupedValue
from domain.value.condition import Condition
from domain.repository.ssq_repository import SSQRepository
from domain.value.time_point import TimePoint
from domain.value.ssq import SSQValueType
from typing import List, Dict
from collections import defaultdict
from application.port.output.progress_output_port import ProgressAdvanceOutputPort
from application.dto.collector import from_ssq_value_type


# from application.dto.collector import
# TODO 変換ロジック
class SSQDiffCollector(Collector):
    def __init__(
        self,
        ssq_repo: SSQRepository,
        value_type: SSQValueType,
        progress_output_port: ProgressAdvanceOutputPort,
    ):
        super().__init__()
        self.ssq_repo = ssq_repo
        self.value_type = value_type
        self.progress_output_port = progress_output_port

    def collect(self, subjects: List[Subject]) -> GroupedValue:

        result: Dict[Condition, Dict[SubjectData, float]] = defaultdict(lambda: dict())

        length = sum(len(subject.sessions) for subject in subjects)
        count = 0

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
                self.progress_output_port.on_advanced(
                    from_ssq_value_type(self.value_type),
                    count,
                    length,
                )

        grouped = GroupedValue(f"ssq_diff_{self.value_type}", dict(result))

        return grouped

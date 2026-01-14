from application.service.collector.collector import Collector
from domain.value.subject import Subject
from domain.value.subject_data import SubjectData
from domain.value.grouped_value import GroupedValue
from domain.value.condition import Condition
from domain.repository.fms_repository import FMSRepository
from typing import List, Dict
from collections import defaultdict
from application.port.output.progress_output_port import ProgressAdvanceOutputPort
from application.model.collector import PEAK_FMS
import time


class PeakFMSCollector(Collector):
    def __init__(
        self, fms_repo: FMSRepository, progress_output_port: ProgressAdvanceOutputPort
    ):
        super().__init__()
        self.fms_repo = fms_repo
        self.progress_output_port = progress_output_port

    def collect(self, subjects: List[Subject]) -> GroupedValue:
        result: Dict[Condition, Dict[SubjectData, float]] = defaultdict(lambda: dict())

        length = sum(len(subject.sessions) for subject in subjects)
        count = 0

        for subject in subjects:
            for session in subject.sessions:
                fms = self.fms_repo.get_fms(
                    subject.data.name,
                    session.condition,
                    session.result.fms_timestamp,
                )
                result[session.condition][subject.data] = fms.peak

                count += 1
                self.progress_output_port.on_advanced(
                    PEAK_FMS,
                    count,
                    length,
                )

        grouped = GroupedValue("peak_fms", dict(result))
        return grouped

from application.usecase.service.collector.collector import Collector
from domain.entity.subject import Subject
from domain.value_object.subject_data import SubjectData
from domain.value_object.grouped_value import GroupedValue
from domain.value_object.condition import Condition
from domain.repository.fms_repository import FMSRepository
from typing import List, Dict
from collections import defaultdict
from application.port.output.collect_value_output_port import CollectValueOutputPort
from application.dto.value_type import ValueType


class PeakFMSCollector(Collector):
    def __init__(self, fms_repo: FMSRepository, output_port: CollectValueOutputPort):
        super().__init__()
        self.fms_repo = fms_repo
        self.output_port = output_port

    def collect(self, subjects: List[Subject]) -> GroupedValue:
        self.output_port.on_start(ValueType.PEAK_FMS)
        result: Dict[Condition, Dict[SubjectData, float]] = defaultdict(lambda: dict())

        length = sum(len(subject.sessions) for subject in subjects)
        count = 0

        try:
            for subject in subjects:
                for session in subject.sessions:
                    fms = self.fms_repo.get_fms(
                        subject.data.name,
                        session.condition,
                        session.result.fms_timestamp,
                    )
                    result[session.condition][subject.data] = fms.peak

                    count += 1
                    self.output_port.on_progress(
                        ValueType.PEAK_FMS,
                        count,
                        length,
                    )
        except Exception as e:
            self.output_port.on_error(ValueType.PEAK_FMS, e)

        grouped = GroupedValue(dict(result))
        self.output_port.on_complete(ValueType.PEAK_FMS, grouped)
        return grouped

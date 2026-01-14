from application.service.collector.collector import Collector
from domain.value.subject import Subject
from domain.value.grouped_value import GroupedValue
from typing import List
from domain.repository.body_sway_repository import BodySwayRepository
from application.port.output.progress_output_port import ProgressAdvanceOutputPort
from domain.value.condition import Condition
from domain.value.subject_data import SubjectData
from collections import defaultdict
from typing import Dict
from application.dto.collector import AVERAGE_COP_SPEED


class AverageCOPSpeedCollector(Collector):
    def __init__(
        self,
        body_sway_repository: BodySwayRepository,
        progress_output_port: ProgressAdvanceOutputPort,
    ):
        self.body_sway_repository = body_sway_repository
        self.progress_output_port = progress_output_port

    def collect(self, subjects: List[Subject]) -> GroupedValue:
        result: Dict[Condition, Dict[SubjectData, float]] = defaultdict(lambda: dict())

        length = sum(len(subject.sessions) for subject in subjects)
        count = 0

        for subject in subjects:
            for session in subject.sessions:
                body_sway = self.body_sway_repository.load(
                    subject.data,
                    session.condition,
                    session.result.body_sway_timestamp,
                )
                result[session.condition][subject.data] = body_sway.average_cop_speed

                count += 1
                self.progress_output_port.on_advanced(
                    AVERAGE_COP_SPEED,
                    count,
                    length,
                )

        grouped = GroupedValue("average_cop_speed", dict(result))
        return grouped

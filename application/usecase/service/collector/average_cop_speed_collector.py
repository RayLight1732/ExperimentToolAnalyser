from application.usecase.service.collector.collector import Collector
from domain.entity.subject import Subject
from domain.value_object.grouped_value import GroupedValue
from typing import List
from domain.repository.body_sway_repository import BodySwayRepository
from application.port.output.collect_value_output_port import CollectValueOutputPort
from application.dto.value_type import ValueType
from domain.value_object.condition import Condition
from domain.value_object.subject_data import SubjectData
from collections import defaultdict
from typing import Dict


class AverageCOPSpeedCollector(Collector):
    def __init__(
        self,
        body_sway_repository: BodySwayRepository,
        output_port: CollectValueOutputPort,
    ):
        self.body_sway_repository = body_sway_repository
        self.output_port = output_port

    def collect(self, subjects: List[Subject]) -> GroupedValue:
        self.output_port.on_start(ValueType.AVERAGE_COP_SPEED)
        result: Dict[Condition, Dict[SubjectData, float]] = defaultdict(lambda: dict())

        length = sum(len(subject.sessions) for subject in subjects)
        count = 0

        try:
            for subject in subjects:
                for session in subject.sessions:
                    body_sway = self.body_sway_repository.load(
                        subject.data,
                        session.condition,
                        session.result.body_sway_timestamp,
                    )
                    result[session.condition][
                        subject.data
                    ] = body_sway.average_cop_speed

                    count += 1
                    self.output_port.on_progress(
                        ValueType.AVERAGE_COP_SPEED,
                        count,
                        length,
                    )
        except Exception as e:
            self.output_port.on_error(ValueType.AVERAGE_COP_SPEED, e)

        grouped = GroupedValue("average_cop_speed", dict(result))
        self.output_port.on_complete(ValueType.AVERAGE_COP_SPEED, grouped)
        return grouped

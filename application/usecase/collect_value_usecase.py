from application.usecase.service.collector.peak_fms_collector import PeakFMSCollector
from application.usecase.service.collector.ssq_diff_collector import SSQDiffCollector
from domain.entity.subject import Subject
from typing import List
from application.port.output.collector_factory import CollectorFactory
from application.port.input.collect_value_input_port import CollectValueInputPort
from application.dto.value_type import ValueType
from domain.value_object.grouped_value import GroupedValue


class CollectValueUsecase(CollectValueInputPort):
    def __init__(
        self,
        collector_factory: CollectorFactory,
    ):
        self.collector_factory = collector_factory

    def execute(
        self, subjects: List[Subject], value_type: ValueType
    ) -> GroupedValue[float]:
        return self.collector_factory.get(value_type).collect(subjects)

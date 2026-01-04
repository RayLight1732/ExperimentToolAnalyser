from application.usecase.service.collector.peak_fms_collector import PeakFMSCollector
from application.usecase.service.collector.ssq_diff_collector import SSQDiffCollector
from domain.entity.subject import Subject
from typing import List, Optional
from application.port.output.collector_factory import CollectorFactory
from application.port.output.filter_factory import FilterFactory
from application.port.input.collect_value_input_port import CollectValueInputPort
from application.dto.value_type import ValueType
from domain.value_object.grouped_value import GroupedValue
from application.dto.filter_parameter import FilterParameter


class CollectValueUsecase(CollectValueInputPort):
    def __init__(
        self, collector_factory: CollectorFactory, filter_factory: FilterFactory
    ):
        self.collector_factory = collector_factory
        self.filter_factory = filter_factory

    def execute(
        self,
        subjects: List[Subject],
        value_type: ValueType,
        filter_parameter: Optional[FilterParameter] = None,
    ) -> GroupedValue:
        raw = self.collector_factory.get(value_type).collect(subjects)
        if filter_parameter is not None:
            return self.filter_factory.get(filter_parameter.type).filter(
                raw, filter_parameter.param
            )
        else:
            return raw

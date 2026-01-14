from application.service.collector.collector_factory import CollectorFactory
from application.dto.value_type import ValueType
from application.service.collector.collector import Collector

from typing import Dict
from bootstrap.context import AppContext
from application.port.output.progress_output_port import ProgressAdvanceOutputPort

from application.service.collector.average_cop_speed_collector import (
    AverageCOPSpeedCollector,
)
from application.service.collector.peak_fms_collector import PeakFMSCollector
from application.service.collector.ssq_diff_collector import SSQDiffCollector
from domain.value.ssq import SSQValueType


class CollectorFactoryImpl(CollectorFactory):
    def __init__(self, collectors: Dict[ValueType, Collector]) -> None:
        self.collectors = collectors

    def get(self, value_type: ValueType) -> Collector:
        return self.collectors[value_type]


def new_collector_factory(
    context: AppContext, progress_advance_output_port: ProgressAdvanceOutputPort
) -> CollectorFactory:
    factory = CollectorFactoryImpl(
        {
            ValueType.PEAK_FMS: PeakFMSCollector(
                context.fms_repository,
                progress_advance_output_port,
            ),
            ValueType.AVERAGE_COP_SPEED: AverageCOPSpeedCollector(
                context.body_sway_repository, progress_advance_output_port
            ),
            ValueType.SSQ_NAUSEA: SSQDiffCollector(
                context.ssq_repository,
                SSQValueType.NAUSEA,
                progress_advance_output_port,
            ),
            ValueType.SSQ_DISORIENTATION: SSQDiffCollector(
                context.ssq_repository,
                SSQValueType.DISORIENTATION,
                progress_advance_output_port,
            ),
            ValueType.SSQ_OCULOMOTOR: SSQDiffCollector(
                context.ssq_repository,
                SSQValueType.OCULOMOTOR,
                progress_advance_output_port,
            ),
            ValueType.SSQ_TOTAL: SSQDiffCollector(
                context.ssq_repository,
                SSQValueType.TOTAL,
                progress_advance_output_port,
            ),
        }
    )

    return factory

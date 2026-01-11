from application.service.collector.collector_factory import CollectorFactory
from application.model.value_type import ValueType
from application.service.collector.collector import Collector


class CollectorFactoryImpl(CollectorFactory):

    def __init__(
        self,
        peak_fms_collector: Collector,
        average_cop_speed_collector: Collector,
        ssq_nausea_diff_collector: Collector,
        ssq_oculomotor_diff_collector: Collector,
        ssq_disorientation_diff_collector: Collector,
        ssq_total_diff_collector: Collector,
    ):
        self._collectors = {
            ValueType.PEAK_FMS: peak_fms_collector,
            ValueType.AVERAGE_COP_SPEED: average_cop_speed_collector,
            ValueType.SSQ_NAUSEA: ssq_nausea_diff_collector,
            ValueType.SSQ_OCULOMOTOR: ssq_oculomotor_diff_collector,
            ValueType.SSQ_DISORIENTATION: ssq_disorientation_diff_collector,
            ValueType.SSQ_TOTAL: ssq_total_diff_collector,
        }

    def get(self, value_type: ValueType) -> Collector:
        try:
            return self._collectors[value_type]
        except KeyError:
            raise ValueError(f"Unsupported ValueType: {value_type}")

from enum import Enum
from domain.value.ssq import SSQValueType


class ValueType(Enum):
    PEAK_FMS = "peak_fms"
    SSQ_NAUSEA = "ssq_nausea"
    SSQ_OCULOMOTOR = "ssq_oculomotor"
    SSQ_DISORIENTATION = "ssq_disorientation"
    SSQ_TOTAL = "ssq_total"
    AVERAGE_COP_SPEED = "average_cop_speed"

    @staticmethod
    def from_ssq_value_type(ssq_value_type: SSQValueType) -> "ValueType":
        mapping = {
            SSQValueType.NAUSEA: ValueType.SSQ_NAUSEA,
            SSQValueType.OCULOMOTOR: ValueType.SSQ_OCULOMOTOR,
            SSQValueType.DISORIENTATION: ValueType.SSQ_DISORIENTATION,
            SSQValueType.TOTAL: ValueType.SSQ_TOTAL,
        }
        if ssq_value_type not in mapping:
            raise ValueError(f"Invalid SSQ value type: {ssq_value_type}")
        return mapping[ssq_value_type]

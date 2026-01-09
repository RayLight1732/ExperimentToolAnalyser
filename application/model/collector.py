from domain.value.ssq import SSQValueType
from application.model.progress_phase import ProgressPhase
from application.model.processing_category import ProcessingCategory

PEAK_FMS = ProgressPhase("holm",ProcessingCategory.COLLECT)
SSQ_NAUSEA = ProgressPhase("ssq_nausea",ProcessingCategory.COLLECT)
SSQ_OCULOMOTOR = ProgressPhase("ssq_oculomotor",ProcessingCategory.COLLECT)
SSQ_DISORIENTATION = ProgressPhase("ssq_disorientation",ProcessingCategory.COLLECT)
SSQ_TOTAL = ProgressPhase("ssq_total",ProcessingCategory.COLLECT)
AVERAGE_COP_SPEED = ProgressPhase("average_cop_speed",ProcessingCategory.COLLECT)

def from_ssq_value_type(ssq_value_type: SSQValueType) -> ProgressPhase:
        mapping = {
            SSQValueType.NAUSEA: SSQ_NAUSEA,
            SSQValueType.OCULOMOTOR: SSQ_OCULOMOTOR,
            SSQValueType.DISORIENTATION: SSQ_DISORIENTATION,
            SSQValueType.TOTAL: SSQ_TOTAL,
        }
        if ssq_value_type not in mapping:
            raise ValueError(f"Invalid SSQ value type: {ssq_value_type}")
        return mapping[ssq_value_type]

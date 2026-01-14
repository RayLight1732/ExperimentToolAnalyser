from domain.value.ssq import SSQValueType
from application.model.progress_phase import ProgressPhase
from application.model.inferential_analysis_step import InferentialAnalysisStep

PEAK_FMS = ProgressPhase("peak_fms", InferentialAnalysisStep.COLLECT_VALUES)
SSQ_NAUSEA = ProgressPhase("ssq_nausea", InferentialAnalysisStep.COLLECT_VALUES)
SSQ_OCULOMOTOR = ProgressPhase("ssq_oculomotor", InferentialAnalysisStep.COLLECT_VALUES)
SSQ_DISORIENTATION = ProgressPhase(
    "ssq_disorientation", InferentialAnalysisStep.COLLECT_VALUES
)
SSQ_TOTAL = ProgressPhase("ssq_total", InferentialAnalysisStep.COLLECT_VALUES)
AVERAGE_COP_SPEED = ProgressPhase(
    "average_cop_speed", InferentialAnalysisStep.COLLECT_VALUES
)


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

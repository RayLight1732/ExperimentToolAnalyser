from enum import Enum


class InferentialAnalysisStep(Enum):
    FILTER_SUBJECTS = "FILTER_SUBJECTS"
    COLLECT_VALUES = "COLLECT_VALUES"
    CALCULATE = "CALCULATE"
    POST_PROCESS = "POST_PROCESS"

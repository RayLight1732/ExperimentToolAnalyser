from enum import Enum

class ProcessingCategory(Enum):
    COLLECT = "collect"
    CALCULATE = "calculate"
    POSTPROCESS = "postprocess"
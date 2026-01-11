from enum import Enum,auto

class MetricType(Enum):
    MEAN = auto()
    STANDARD_DEVIATION = auto()
    STANDARD_ERROR = auto()
    DEVIATION = auto()
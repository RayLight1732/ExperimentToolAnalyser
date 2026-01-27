from enum import Enum,auto

class TestType(Enum):
    PAIRED_T_TEST = auto()
    WILCOXON_TEST = auto()
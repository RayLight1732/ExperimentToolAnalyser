from dataclasses import dataclass
from typing import Tuple,ClassVar
from domain.value.fms_format_error import FMSFormatError

@dataclass(frozen=True)
class FMS:
    ANSWER_COUNT: ClassVar[int] = 5
    MIN_VALUE: ClassVar[int] = 0
    MAX_VALUE: ClassVar[int] = 20

    values: Tuple[int, ...]

    def __post_init__(self):
        if len(self.values) != self.ANSWER_COUNT:
            raise FMSFormatError()

        for v in self.values:
            if not (self.MIN_VALUE <= v <= self.MAX_VALUE):
                raise FMSFormatError()
            
    @property
    def peak(self):
        return max(self.values)
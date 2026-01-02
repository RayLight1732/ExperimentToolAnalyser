from typing import Sequence,Tuple
from dataclasses import dataclass
from domain.value_object.fms import FMS
from domain.error.fms_format_error import FMSFormatError

@dataclass(frozen=True)
class FMSCsv:
    answers: Tuple[int, ...]

    @classmethod
    def from_csv_row(cls, row: Sequence[str]) -> "FMSCsv":
        if len(row) != FMS.ANSWER_COUNT:
            raise FMSFormatError()
        
        # might be raised ValueError
        answers = tuple(int(v) for v in row)
        return cls(answers)

    def to_domain(self) -> FMS:
        return FMS(self.answers)
from typing import Sequence,Tuple
from dataclasses import dataclass
from domain.value_object.ssq import SSQ
from domain.error.ssq_format_error import SSQFormatError

@dataclass(frozen=True)
class SSQCsv:
    answers: Tuple[int, ...]

    @classmethod
    def from_csv_row(cls, row: Sequence[str]) -> "SSQCsv":
        if len(row) != SSQ.ANSWER_COUNT:
            raise SSQFormatError()
        
        # might be raised ValueError
        answers = tuple(int(v) for v in row)
        return cls(answers)

    def to_domain(self) -> SSQ:
        return SSQ(self.answers)
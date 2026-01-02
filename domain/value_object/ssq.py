from dataclasses import dataclass
from typing import Tuple,ClassVar
from domain.error.ssq_format_error import SSQFormatError
from enum import Enum,auto
class SSQValueType(Enum):
    Nausea = auto()
    Oculomotor=auto()
    Disorientation=auto()
    Total=auto()


@dataclass(frozen=True)
class SSQ:
    ANSWER_COUNT: ClassVar[int] = 16
    MIN_VALUE: ClassVar[int] = 0
    MAX_VALUE: ClassVar[int] = 4

    values: Tuple[int, ...]

    def __post_init__(self):
        if len(self.values) != self.ANSWER_COUNT:
            raise SSQFormatError()

        for v in self.values:
            if not (self.MIN_VALUE <= v <= self.MAX_VALUE):
                raise SSQFormatError()
            
    def get_value(self,type:SSQValueType)->float:
        if type == SSQValueType.Nausea:
            return self.nausea
        elif type == SSQValueType.Oculomotor:
            return self.oculomotor
        elif type == SSQValueType.Disorientation:
            return self.disorientation
        elif type == SSQValueType.Total:
            return self.tortal
        else:
            raise ValueError("the type is not exists")
            
    @property
    def nausea(self):
        condition = [1,6,7,8,9,15,16]
        return sum([v for i,v in enumerate(self.values) if i+1 in condition])*9.54
    
    @property
    def oculomotor(self):
        condition = [1,2,3,4,5,9,11]
        return sum([v for i,v in enumerate(self.values) if i+1 in condition])*7.58
    
    @property
    def disorientation(self):
        condition = [5,8,10,11,12,13,14]
        return sum([v for i,v in enumerate(self.values) if i+1 in condition])*13.92

    @property
    def tortal(self):
        return sum(self.values)*3.74
    
    
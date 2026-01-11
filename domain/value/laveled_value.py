from dataclasses import dataclass
from typing import List, Any


@dataclass(frozen=True)
class LaveledValue:
    lavel: str
    value: List[Any]


@dataclass(frozen=True)
class LaveledValues:
    values: List[LaveledValue]

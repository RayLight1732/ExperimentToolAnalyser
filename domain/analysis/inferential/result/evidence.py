from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Evidence:
    p_value: float
    statistic: Optional[float] = None
    effect_size: Optional[float] = None

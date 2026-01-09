from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class Evidence:
    statistic: Optional[float]
    p_value: float
    effect_size: Optional[float] = None
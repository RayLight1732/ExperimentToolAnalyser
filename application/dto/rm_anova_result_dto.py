from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RMAnovaResult:
    anova_table: Any

from dataclasses import dataclass
from application.dto.filter_type import FilterType
from typing import Any


@dataclass(frozen=True)
class FilterParameter:
    type: FilterType
    param: Any

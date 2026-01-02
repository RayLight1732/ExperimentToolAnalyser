from dataclasses import dataclass
from typing import TypeVar,Generic,Dict
from domain.value_object.condition import Condition

T = TypeVar("T")

@dataclass(frozen=True)
class ByCondition(Generic[T]):
    values: Dict[Condition, T]
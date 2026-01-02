from dataclasses import dataclass
from typing import TypeVar,Generic,Dict,Tuple
from domain.value_object.condition import Condition

T = TypeVar("T")

@dataclass(frozen=True)
class ByConditionPair(Generic[T]):
    values: Dict[Tuple[Condition,Condition], T]
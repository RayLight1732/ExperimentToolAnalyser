from dataclasses import dataclass
from typing import Optional,List
from domain.entity.subject import Session
from domain.value_object.condition import Condition

@dataclass(frozen=True)
class SessionFetchResult:
    success: bool
    session: Optional[Session] = None
    missing_conditions: List[Condition] = []
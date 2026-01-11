from dataclasses import dataclass
from typing import Optional, List
from domain.value.subject import Session
from domain.value.condition import Condition


@dataclass(frozen=True)
class SessionFetchResult:
    success: bool
    session: Optional[Session] = None
    missing_conditions: List[Condition] = []

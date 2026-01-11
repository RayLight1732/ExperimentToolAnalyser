from dataclasses import dataclass
from typing import Optional
from domain.value.condition import Condition


# TODO Optionalにするとやりにくい
@dataclass(frozen=True)
class Comparison:
    left: Optional[Condition]
    right: Optional[Condition]

    @staticmethod
    def global_() -> "Comparison":
        return Comparison(None, None)

    @property
    def is_global(self) -> bool:
        return self.left is None and self.right is None

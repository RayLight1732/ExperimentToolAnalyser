from dataclasses import dataclass
from turtle import left
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
    
    def to_label(self,show_position:bool) -> str:
        if self.is_global:
            return "global"
        elif show_position:
            return f"{self.left}-{self.right}"
        else:
            return f"{self.left.mode.display_name}-{self.right.mode.display_name}"

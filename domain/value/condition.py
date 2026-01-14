from enum import Enum
from dataclasses import dataclass
from typing import Optional, Iterable


class CoolingMode(Enum):
    NONE = "なし"
    PERIODIC = "周期的"
    SICK_SCENE_ONLY = "酔いやすい場面のみ"
    ALWAYS = "常時"

    @property
    def display_name(self) -> str:
        return self.value

    @property
    def requires_position(self) -> bool:
        return self is not CoolingMode.NONE


class Position(Enum):
    CAROTID = "頸動脈"
    NECK = "首筋"

    @property
    def display_name(self) -> str:
        return self.value


@dataclass(frozen=True)
class Condition:
    mode: CoolingMode
    position: Optional[Position] = None

    def __post_init__(self):
        if self.mode.requires_position and self.position is None:
            raise ValueError("position is required for this mode")

        if not self.mode.requires_position and self.position is not None:
            raise ValueError("position must be None for this mode")

    def __str__(self) -> str:
        if self.position is None:
            return f"{self.mode.display_name}"
        return f"{self.mode.display_name}/{self.position.display_name}"

    @staticmethod
    def all_same_position(conditions: Iterable["Condition"]) -> bool:
        positions = {c.position for c in conditions if c.position is not None}
        return len(positions) <= 1

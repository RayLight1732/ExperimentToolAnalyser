from dataclasses import dataclass
import math
from functools import cached_property


@dataclass(frozen=True)
class COP:
    x: float
    y: float
    time: float


@dataclass(frozen=True)
class BodySway:
    cop_points: list[COP]

    @property
    def frequency(self) -> float:
        if len(self.cop_points) < 2:
            return 0.0
        total_time = self.cop_points[-1].time - self.cop_points[0].time
        if total_time <= 0:
            return 0.0
        return (len(self.cop_points) - 1) / total_time

    @cached_property
    def average_cop_speed(self) -> float:
        if len(self.cop_points) < 2:
            return 0.0

        total_distance = 0.0

        for prev, curr in zip(self.cop_points, self.cop_points[1:]):
            dx = curr.x - prev.x
            dy = curr.y - prev.y
            distance = math.hypot(dx, dy)
            total_distance += distance

        total_time = self.cop_points[-1].time - self.cop_points[0].time
        if total_time <= 0:
            return 0.0

        return total_distance / total_time

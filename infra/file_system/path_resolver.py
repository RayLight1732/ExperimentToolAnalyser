from domain.value_object.condition import Condition
from datetime import datetime
from domain.value_object.time_point import TimePoint
import os


class PathResolver:
    def __init__(self, working_dir: str):
        self.working_dir = working_dir

    def subject_path(self, subject_name: str, condition: Condition) -> str:
        if condition.mode.requires_position and condition.position is not None:
            return os.path.join(
                self.working_dir,
                condition.mode.display_name,
                condition.position.display_name,
                subject_name,
            )
        return os.path.join(
            self.working_dir,
            condition.mode.display_name,
            condition.mode.display_name,
            subject_name,
        )

    def ssq_path(
        self,
        subject_name: str,
        condition: Condition,
        time_point: TimePoint,
        timestamp: datetime,
    ) -> str:
        base = self.subject_path(subject_name, condition)
        formatted = timestamp.strftime("%Y%m%d_%H%M%S")
        return os.path.join(base, f"SSQ_{formatted}_{time_point.display_name}.csv")

    def fms_path(
        self, subject_name: str, condition: Condition, timestamp: datetime
    ) -> str:
        base = self.subject_path(subject_name, condition)
        formatted = timestamp.strftime("%Y%m%d_%H%M%S")
        return os.path.join(base, f"FMS_{formatted}.csv")

    def body_sway_path(
        self, subject_name: str, condition: Condition, timestamp: datetime
    ) -> str:
        base = self.subject_path(subject_name, condition)
        formatted = timestamp.strftime("%y%m%d%H%M%S")
        return os.path.join(base, f"{formatted}.csv")

    def mean_and_se_path(self, name: str) -> str:
        return os.path.join(self.working_dir, name)

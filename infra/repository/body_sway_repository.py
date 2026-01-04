from domain.repository.body_sway_repository import (
    BodySwayRepository as IBodySwayRepository,
)
from domain.value_object.condition import Condition
from infra.dto.fms_csv import FMSCsv
from infra.file_system.path_resolver import PathResolver
from infra.file_system.file_system import FileSystem
from datetime import datetime
from domain.value_object.body_sway import BodySway, COP
from typing import List
from domain.error.body_sway_not_found_error import BodySwayNotFoundError


class BodySwayRepository(IBodySwayRepository):
    def __init__(self, path_resolver: PathResolver, file_system: FileSystem):
        self.path_resolver = path_resolver
        self.file_system = file_system

    def load(self, name: str, condition: Condition, timestamp: datetime):
        try:
            path = self.path_resolver.body_sway_path(name, condition, timestamp)
        except Exception as e:
            # TODO: 詳細な例外を捕捉する
            raise BodySwayNotFoundError(name) from e

        cop_points: List[COP] = []

        rows = self.file_system.load_csv(path)

        # 1行目（ヘッダ）を読み飛ばす
        header_skipped = False
        for row in rows:
            if not header_skipped:
                header_skipped = True
                continue

            time = float(row[0])
            x = float(row[1])
            y = float(row[2])

            cop_points.append(
                COP(
                    x=x,
                    y=y,
                    time=time,
                )
            )

        return BodySway(cop_points=cop_points)

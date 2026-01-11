from domain.repository.body_sway_repository import (
    BodySwayRepository as IBodySwayRepository,
)
from domain.value.condition import Condition
from infra.file_system.path_resolver import PathResolver
from infra.file_system.file_system import FileSystem
from datetime import datetime
from domain.value.body_sway import BodySway, COP
from typing import List
from domain.repository.error.body_sway_not_found_error import BodySwayNotFoundError
from domain.repository.error.body_sway_format_error import BodySwayFormatError
from domain.value.subject_data import SubjectData


class BodySwayRepository(IBodySwayRepository):
    def __init__(self, path_resolver: PathResolver, file_system: FileSystem):
        self.path_resolver = path_resolver
        self.file_system = file_system

    def load(
        self, subject_data: SubjectData, condition: Condition, timestamp: datetime
    ):
        try:
            path = self.path_resolver.body_sway_path(
                subject_data.name, condition, timestamp
            )
        except Exception as e:
            raise BodySwayNotFoundError(subject_data, condition, timestamp) from e

        cop_points: List[COP] = []

        rows = self.file_system.load_csv(path)
        rows_iter = iter(rows)

        # ヘッダをスキップ
        try:
            next(rows_iter)
        except StopIteration:
            return BodySway(cop_points=[])

        for row in rows_iter:
            # 空行チェック
            if not row or all(cell.strip() == "" for cell in row):
                # ★ 次の行が存在するか確認
                try:
                    next(rows_iter)
                except StopIteration:
                    # 最後の行なので許可
                    break
                else:
                    # 途中の空行は仕様違反
                    raise BodySwayFormatError(subject_data, condition, timestamp)

            try:
                time = float(row[0])
                x = float(row[1])
                y = float(row[2])
            except Exception as e:
                raise BodySwayFormatError(subject_data, condition, timestamp) from e

            cop_points.append(
                COP(
                    x=x,
                    y=y,
                    time=time,
                )
            )

        return BodySway(cop_points=cop_points)

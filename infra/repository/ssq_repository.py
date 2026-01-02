from domain.repository.ssq_repository import SSQRepository as ISSQRepository
from domain.value_object.condition import Condition
from domain.value_object.time_point import TimePoint
from infra.dto.ssq_csv import SSQCsv
from infra.file_system.path_resolver import PathResolver
from infra.file_system.file_system import FileSystem
from datetime import datetime
from domain.value_object.ssq import SSQ
from typing import Optional
from domain.error.ssq_not_found_error import SSQNotFoundError
from infra.repository.internal.single_row_repository import SingleRowCsvRepository


class SSQRepository(SingleRowCsvRepository[SSQ], ISSQRepository):
    def get_ssq(
        self,
        name: str,
        condition: Condition,
        time_point: TimePoint,
        timestamp: datetime,
    ):
        path = self.path_resolver.ssq_path(name, condition, time_point, timestamp)
        return self._load_single_row(path)

    def _to_domain(self, row) -> SSQ:
        return SSQCsv.from_csv_row(row).to_domain()

    def _not_found_error(self, path: str) -> Exception:
        return SSQNotFoundError(path)

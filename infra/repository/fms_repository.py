from domain.repository.fms_repository import FMSRepository as IFMSRepository
from domain.value_object.condition import Condition
from infra.dto.fms_csv import FMSCsv
from infra.file_system.path_resolver import PathResolver
from infra.file_system.file_system import FileSystem
from datetime import datetime
from domain.value_object.fms import FMS
from domain.error.fms_not_found_error import FMSNotFoundError
from infra.repository.internal.single_row_repository import SingleRowCsvRepository

class FMSRepository(SingleRowCsvRepository[FMS], IFMSRepository):
    def get_fms(self, name:str, condition:Condition, timestamp:datetime):
        path = self.path_resolver.fms_path(name, condition, timestamp)
        return self._load_single_row(path)

    def _to_domain(self, row) -> FMS:
        return FMSCsv.from_csv_row(row).to_domain()

    def _not_found_error(self, path: str) -> Exception:
        return FMSNotFoundError(path)

def new_fms_repository(path_resolver:PathResolver,file_system:FileSystem)->IFMSRepository:
    return FMSRepository(path_resolver,file_system)
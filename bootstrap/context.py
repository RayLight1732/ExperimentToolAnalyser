from bootstrap.config import Config
from infra.file_system.file_system import OSFileSystem
from infra.file_system.path_resolver import PathResolver
from infra.repository.fms_repository import FMSRepository
from infra.repository.ssq_repository import SSQRepository
from infra.repository.body_sway_repository import BodySwayRepository
from infra.repository.laveled_value_repository import LaveledValueRepository
from infra.file_system.file_name_parser import FileNameParser
from infra.file_system.experiment_file_index import ExperimentFileIndex
from infra.repository.subject_repository import SubjectRepository
from infra.repository.session_repository import SessionRepository
from infra.calculator.inferential.paired_t_test_calculator import PairedTTestCalculator
from infra.calculator.inferential.rm_anova_calculator import RMAnovaCalculator

class AppContext:
    def __init__(self, config: Config):
        self.config = config
        self.parser = FileNameParser()
        self.file_system = OSFileSystem()
        self.path_resolver = PathResolver(config.working_dir)
        self.save_path_resolver = PathResolver(config.save_dir)

        self.fms_repository = FMSRepository(self.path_resolver, self.file_system)
        self.ssq_repository = SSQRepository(self.path_resolver, self.file_system)
        self.body_sway_repository = BodySwayRepository(
            self.path_resolver, self.file_system
        )
        self.laveled_value_repository = LaveledValueRepository(
            self.save_path_resolver, self.file_system
        )
        self.file_index = ExperimentFileIndex(
            self.file_system, self.path_resolver, self.parser
        )
        self.session_repository = SessionRepository(self.file_index)
        self.subject_repository = SubjectRepository(
            self.file_index, self.session_repository
        )

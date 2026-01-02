from usecase.completed_subject_find_usecase import (
    CompletedSubjectFindUsecaseInterface,
    CompletedSubjectFindUsecase,
)
from infra.repository.session_repository import new_session_repository
from infra.repository.subject_repository import new_subject_repository
from infra.repository.fms_repository import FMSRepository
from infra.file_system.file_system import OSFileSystem
from infra.file_system.path_resolver import PathResolver
from bootstrap.config import Config
from infra.file_system.experiment_file_index import new_experiment_file_index
from usecase.service.calculator.mean_calculator import MeanCalculator
from usecase.service.calculator.rm_anova_calculator import (
    RMAnovaCalculator,
    AnovaResults,
)
from usecase.service.calculator.mean_and_se_calculator import MeanAndSECalculator
from usecase.service.calculator.paired_t_test_with_holm_calculator import (
    PairedTTestWithHolmCalculator,
    CorrectedAndOriginalValueByConditionPair,
)
from usecase.service.collector.peak_fms_collector import PeakFMSCollector
from usecase.statistics_usecase import StatisticsUsecaseInterface, StatisticsUsecase
from domain.analysis.result.mean_and_se import MeanByCondition, MeanAndSEByCondition
from infra.repository.ssq_repository import SSQRepository


class AppContext:
    def __init__(self, config: Config):
        self.config = config
        self.file_system = OSFileSystem()
        self.path_resolver = PathResolver(config.working_dir)

        self.fms_repository = FMSRepository(self.path_resolver, self.file_system)
        self.ssq_repository = SSQRepository(self.path_resolver, self.file_system)


def new_completed_subject_find_usecase(
    config: Config,
) -> CompletedSubjectFindUsecaseInterface:
    file_index = new_experiment_file_index(config)
    session_repo = new_session_repository(file_index)
    subject_repo = new_subject_repository(file_index, session_repo)
    return CompletedSubjectFindUsecase(subject_repo)


def new_mean_peak_fms_calculate_usecase(
    config: Config,
) -> StatisticsUsecaseInterface[MeanByCondition]:
    calculator = MeanCalculator()
    path_resolver = PathResolver(config.working_dir)
    file_system = OSFileSystem()
    fms_repo = FMSRepository(path_resolver, file_system)
    collector = PeakFMSCollector(fms_repo)

    return StatisticsUsecase[MeanByCondition](collector, calculator)


def new_peak_fms_anova_usecase(
    config: Config,
) -> StatisticsUsecaseInterface[AnovaResults]:
    calculator = RMAnovaCalculator()
    path_resolver = PathResolver(config.working_dir)
    file_system = OSFileSystem()
    fms_repo = FMSRepository(path_resolver, file_system)
    collector = PeakFMSCollector(fms_repo)

    return StatisticsUsecase[AnovaResults](collector, calculator)


def new_mean_and_se_fms_usecase(
    config: Config,
) -> StatisticsUsecaseInterface[MeanAndSEByCondition]:
    calculator = MeanAndSECalculator()
    path_resolver = PathResolver(config.working_dir)
    file_system = OSFileSystem()
    fms_repo = FMSRepository(path_resolver, file_system)
    collector = PeakFMSCollector(fms_repo)

    return StatisticsUsecase[MeanAndSEByCondition](collector, calculator)


def new_peak_fms_paired_t_test_with_holm_calculator(
    config: Config,
) -> StatisticsUsecaseInterface[CorrectedAndOriginalValueByConditionPair]:
    calculator = PairedTTestWithHolmCalculator()
    path_resolver = PathResolver(config.working_dir)
    file_system = OSFileSystem()
    fms_repo = FMSRepository(path_resolver, file_system)
    collector = PeakFMSCollector(fms_repo)

    return StatisticsUsecase[CorrectedAndOriginalValueByConditionPair](
        collector, calculator
    )


def all_value_getter(config: Config):
    calculator = PairedTTestWithHolmCalculator()
    path_resolver = PathResolver(config.working_dir)
    file_system = OSFileSystem()
    fms_repo = FMSRepository(path_resolver, file_system)
    collector = PeakFMSCollector(fms_repo)

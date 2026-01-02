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
from domain.service.collector import Collector
from domain.service.calculator import Calculator
from infra.repository.ssq_repository import SSQRepository
from usecase.service.operation_registory import (
    new_operation_registory,
    ValueType,
    CalculationType,
)
from typing import Dict


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


def new_statistics_usecase(config: Config) -> StatisticsUsecaseInterface:
    path_resolver = PathResolver(config.working_dir)
    file_system = OSFileSystem()
    fms_repo = FMSRepository(path_resolver, file_system)

    collectors: Dict[ValueType, Collector] = {}
    collectors[ValueType.FMS] = PeakFMSCollector(fms_repo)

    calculators: Dict[CalculationType, Calculator] = {}
    calculators[CalculationType.MEAN] = MeanCalculator()
    calculators[CalculationType.MEAN_AND_SE] = MeanAndSECalculator()
    calculators[CalculationType.RM_ANOVA] = RMAnovaCalculator()
    calculators[CalculationType.PAIRED_T_TEST_WITH_HOLM] = (
        PairedTTestWithHolmCalculator()
    )

    registory = new_operation_registory(config, collectors, calculators)
    return StatisticsUsecase(registory)

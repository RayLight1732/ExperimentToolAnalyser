from application.orchestrator.statistics_orchestrator import StatisticsOrchestrator
from application.port.input.list_completed_subjects_input_port import (
    ListCompletedSubjectInputPort,
)
from application.port.input.statistics_usecase_input_port import (
    StatisticsUsecaseInputPort,
)
from application.usecase.list_completed_subjects_usecase import (
    ListCompletedSubjectsUsecase,
)
from application.port.input.statistics_usecase_input_port import (
    StatisticsUsecaseInputPort,
)
from application.port.output.calculator.calculate_mean_and_se_output_port import (
    CalculateMeanAndSEOutputPort,
)
from application.usecase.calculator.calculate_mean_and_se_usecase import (
    CalculateMeanAndSEUsecase,
)
from application.port.input.collect_value_input_port import (
    CollectValueInputPort,
)
from application.port.output.calculator.calculate_mean_and_se_output_port import (
    CalculateMeanAndSEOutputPort,
)
from application.port.output.calculator.run_rm_anova_output_port import (
    RunRMAnovaOutputPort,
)
from application.usecase.calculator.run_rm_anova_calculator import RunRMAnovaUsecase
from application.usecase.calculator.run_paired_t_test_with_holm_usecase import (
    RunPairedTTestWithHolmUsecase,
)
from application.usecase.collect_value_usecase import CollectValueUsecase
from application.usecase.service.collector.collector_factory import CollectorFactoryImpl
from bootstrap.config import Config
from infra.file_system.experiment_file_index import new_experiment_file_index
from infra.file_system.file_system import OSFileSystem
from infra.file_system.path_resolver import PathResolver
from infra.repository.fms_repository import FMSRepository
from infra.repository.session_repository import new_session_repository
from infra.repository.ssq_repository import SSQRepository
from infra.repository.subject_repository import new_subject_repository
from infra.repository.body_sway_repository import BodySwayRepository
from presentation.controller.statistics_controller import StatisticsController
from application.usecase.service.collector.peak_fms_collector import PeakFMSCollector
from application.usecase.service.collector.ssq_diff_collector import SSQDiffCollector
from domain.value_object.ssq import SSQValueType
from application.port.output.collect_value_output_port import (
    CollectValueOutputPort,
)
from application.port.output.calculator.run_paired_t_test_with_holm_output_port import (
    RunPairedTTestWithHolmOutputPort,
)
from application.usecase.service.collector.average_cop_speed_collector import (
    AverageCOPSpeedCollector,
)
from application.usecase.service.collector.filter.filter_factory import (
    FilterFactoryImpl,
)
from application.usecase.service.collector.filter.name_filter import NameFilter
from application.usecase.save_calculation_result_usecase import (
    SaveCalculationResultUsecase,
)
from infra.repository.laveled_value_repository import LaveledValueRepository


class AppContext:
    def __init__(self, config: Config):
        self.config = config
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


def new_list_completed_subjects_usecase(
    context: AppContext,
) -> ListCompletedSubjectInputPort:
    file_index = new_experiment_file_index(context.config)
    session_repo = new_session_repository(file_index)
    subject_repo = new_subject_repository(file_index, session_repo)
    return ListCompletedSubjectsUsecase(subject_repo)


def new_app_context(config: Config) -> AppContext:
    return AppContext(config)


def new_calculate_mean_and_se_usecase(
    output_port: CalculateMeanAndSEOutputPort,
) -> StatisticsUsecaseInputPort:
    usecase = CalculateMeanAndSEUsecase(output_port)
    return usecase


def new_rm_anova_usecase(
    output_port: RunRMAnovaOutputPort,
) -> StatisticsUsecaseInputPort:
    usecase = RunRMAnovaUsecase(output_port)
    return usecase


def new_paried_t_test_with_holm_usecase(
    output_port: RunPairedTTestWithHolmOutputPort,
) -> StatisticsUsecaseInputPort:

    usecase = RunPairedTTestWithHolmUsecase(output_port)
    return usecase


def new_collect_value_usecase(
    context: AppContext,
    output_port: CollectValueOutputPort,
) -> CollectValueInputPort:
    return CollectValueUsecase(
        collector_factory=CollectorFactoryImpl(
            peak_fms_collector=PeakFMSCollector(
                fms_repo=context.fms_repository,
                output_port=output_port,
            ),
            average_cop_speed_collector=AverageCOPSpeedCollector(
                body_sway_repository=context.body_sway_repository,
                output_port=output_port,
            ),
            ssq_nausea_diff_collector=SSQDiffCollector(
                ssq_repo=context.ssq_repository,
                value_type=SSQValueType.NAUSEA,
                output_port=output_port,
            ),
            ssq_oculomotor_diff_collector=SSQDiffCollector(
                ssq_repo=context.ssq_repository,
                value_type=SSQValueType.OCULOMOTOR,
                output_port=output_port,
            ),
            ssq_disorientation_diff_collector=SSQDiffCollector(
                ssq_repo=context.ssq_repository,
                value_type=SSQValueType.DISORIENTATION,
                output_port=output_port,
            ),
            ssq_total_diff_collector=SSQDiffCollector(
                ssq_repo=context.ssq_repository,
                value_type=SSQValueType.TOTAL,
                output_port=output_port,
            ),
        ),
        filter_factory=FilterFactoryImpl(name_filter=NameFilter()),
    )


def new_statistics_controller(
    context: AppContext,
    mean_and_se_output_port: CalculateMeanAndSEOutputPort,
    paired_t_test_output_port: RunPairedTTestWithHolmOutputPort,
    collect_value_output_port: CollectValueOutputPort,
) -> StatisticsController:
    completed_subjects_usecase = new_list_completed_subjects_usecase(context)
    collect_value_usecase = new_collect_value_usecase(
        context, collect_value_output_port
    )

    mean_and_se_orchestrator = StatisticsOrchestrator(
        new_calculate_mean_and_se_usecase(output_port=mean_and_se_output_port),
        completed_subjects_usecase,
        collect_value_usecase,
    )

    paired_t_test_orchestrator = StatisticsOrchestrator(
        statistics_usecase=new_paried_t_test_with_holm_usecase(
            output_port=paired_t_test_output_port
        ),
        list_completed_subjects_usecase=completed_subjects_usecase,
        collect_value_usecase=collect_value_usecase,
    )
    save_calculation_result_usecase = SaveCalculationResultUsecase(
        context.laveled_value_repository
    )

    return StatisticsController(
        list_completed_subjects_usecase=completed_subjects_usecase,
        mean_and_se_orchestrator=mean_and_se_orchestrator,
        paired_t_test_orchestrator=paired_t_test_orchestrator,
        save_calculation_result_input_port=save_calculation_result_usecase,
    )

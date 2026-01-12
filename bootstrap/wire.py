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
from application.port.input.inferential_statistics_input_port import (
    InferentialStatisticsInputPort,
)
from application.usecase.run_inferential_analysis_usecase import (
    RunInferentialAnalysisUseCase,
)
from domain.value.condition import Condition, Position, CoolingMode

from typing import Callable, List

from application.service.collector.collector_factory import CollectorFactoryImpl
from application.model.value_type import ValueType
from application.service.collector.average_cop_speed_collector import (
    AverageCOPSpeedCollector,
)
from application.service.collector.peak_fms_collector import PeakFMSCollector
from application.service.collector.ssq_diff_collector import SSQDiffCollector
from application.port.output.inferential_statistics_output_port import (
    InferentialResultOutputPort,
)
from application.port.output.progress_output_port import (
    ProgressLifeCycleOutputPort,
)

from application.port.output.progress_output_port import ProgressAdvanceOutputPort
from domain.value.ssq import SSQValueType
from infra.calculator.inferential.paired_t_test_calculator import PairedTTestCalculator
from infra.post_processor.holm_post_processor import HolmPostProcessor
from domain.analysis.inferential.post_processor import PostProcessor
from presentation.cli.controller.cli_controller import CLIController
from presentation.cli.controller.inferential_analysis_cli_controller import (
    InferentialStatisticsCLIController,
)
from infra.calculator.inferential.rm_anova_calculator import RMAnovaCalculator
from infra.calculator.inferential.friedman_calculator import FriedmanCalculator


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


def new_inferential_analysis_usecase_factory(
    context: AppContext,
) -> Callable[
    [
        ProgressLifeCycleOutputPort,
        ProgressAdvanceOutputPort,
        InferentialResultOutputPort,
    ],
    InferentialStatisticsInputPort,
]:
    return lambda progress_cycle_output_port, progress_advance_output_port, inferentional_result_output_port: new_inferential_analysis_usecase(
        context,
        progress_cycle_output_port,
        progress_advance_output_port,
        inferentional_result_output_port,
    )


def new_inferential_analysis_usecase(
    context: AppContext,
    progress_cycle_output_port: ProgressLifeCycleOutputPort,
    progress_advance_output_port: ProgressAdvanceOutputPort,
    inferentional_result_output_port: InferentialResultOutputPort,
):

    required = {
        Condition(CoolingMode.NONE),
        Condition(CoolingMode.ALWAYS, Position.CAROTID),
        Condition(CoolingMode.PERIODIC, Position.CAROTID),
        Condition(CoolingMode.SICK_SCENE_ONLY, Position.CAROTID),
    }

    collector_factory = CollectorFactoryImpl(
        {
            ValueType.PEAK_FMS: PeakFMSCollector(
                context.fms_repository,
                progress_advance_output_port,
            ),
            ValueType.AVERAGE_COP_SPEED: AverageCOPSpeedCollector(
                context.body_sway_repository, progress_advance_output_port
            ),
            ValueType.SSQ_NAUSEA: SSQDiffCollector(
                context.ssq_repository,
                SSQValueType.NAUSEA,
                progress_advance_output_port,
            ),
            ValueType.SSQ_DISORIENTATION: SSQDiffCollector(
                context.ssq_repository,
                SSQValueType.DISORIENTATION,
                progress_advance_output_port,
            ),
            ValueType.SSQ_OCULOMOTOR: SSQDiffCollector(
                context.ssq_repository,
                SSQValueType.OCULOMOTOR,
                progress_advance_output_port,
            ),
            ValueType.SSQ_TOTAL: SSQDiffCollector(
                context.ssq_repository,
                SSQValueType.TOTAL,
                progress_advance_output_port,
            ),
        }
    )
    calculator = FriedmanCalculator(progress_advance_output_port)
    post_processors: List[PostProcessor] = [HolmPostProcessor()]
    return RunInferentialAnalysisUseCase(
        required,
        context.subject_repository,
        collector_factory,
        calculator,
        post_processors,
        progress_cycle_output_port,
        inferentional_result_output_port,
    )


def new_cli_controller(config: Config):
    context = AppContext(config)
    inferential_analysis_usecase_factory = new_inferential_analysis_usecase_factory(
        context
    )
    inferential_controller = InferentialStatisticsCLIController(
        inferential_analysis_usecase_factory
    )

    controller = CLIController(inferential_controller)
    return controller

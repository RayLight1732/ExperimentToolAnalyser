from bootstrap.config import Config
from application.port.input.inferential_statistics_input_port import (
    InferentialStatisticsInputPort,
)
from application.usecase.run_inferential_analysis_usecase import (
    RunInferentialAnalysisUseCase,
)
from domain.value.condition import Condition, Position, CoolingMode

from typing import Callable, List

from application.port.output.inferential_statistics_output_port import (
    InferentialResultOutputPort,
)
from application.port.output.progress_output_port import (
    ProgressLifeCycleOutputPort,
)

from application.port.output.progress_output_port import ProgressAdvanceOutputPort
from infra.calculator.inferential.paired_t_test_calculator import PairedTTestCalculator
from infra.calculator.inferential.wilcoxon_calculator import WilcoxonCalculator
from infra.post_processor.holm_post_processor import HolmPostProcessor
from domain.analysis.inferential.post_processor import PostProcessor
from adapter.controller.cli_controller import CLIController
from adapter.controller.inferential_analysis_cli_controller import (
    InferentialStatisticsCLIController,
)
from application.service.collector.collector_factory_impl import new_collector_factory
from infra.calculator.inferential.friedman_calculator import FriedmanCalculator
from bootstrap.context import AppContext
from infra.strage.file_graph_storage import FileGraphStorage
from application.usecase.plot_data_usecase import PlotDataUseCase
from infra.graph.spaghetti_plot_generator import SpaghettiPlotGenerator
from adapter.controller.plot_cli_controller import PlotCLIController
from infra.graph.box_plot_generator import BoxPlotGenerator

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

    collector_factory = new_collector_factory(context, progress_advance_output_port)
    calculator = WilcoxonCalculator(progress_advance_output_port)
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


def new_spaghetti_plot_usecase_factory(
    context: AppContext,
) -> Callable[
    [
        ProgressLifeCycleOutputPort,
        ProgressAdvanceOutputPort,
    ],
    PlotDataUseCase,
]:
    return lambda progress_cycle_output_port, progress_advance_output_port: new_spaghetti_plot_usecase(
        context,
        progress_cycle_output_port,
        progress_advance_output_port,
    )


def new_spaghetti_plot_usecase(
    context: AppContext,
    progress_cycle_output_port: ProgressLifeCycleOutputPort,
    progress_advance_output_port: ProgressAdvanceOutputPort,
):

    required = {
        Condition(CoolingMode.NONE),
        Condition(CoolingMode.ALWAYS, Position.CAROTID),
        Condition(CoolingMode.PERIODIC, Position.CAROTID),
        Condition(CoolingMode.SICK_SCENE_ONLY, Position.CAROTID),
        Condition(CoolingMode.ALWAYS_STRONG,Position.CAROTID)
    }

    collector_factory = new_collector_factory(context, progress_advance_output_port)
    generators = [SpaghettiPlotGenerator(),BoxPlotGenerator()]
    storage = FileGraphStorage(context.config.save_dir)
    return PlotDataUseCase(
        required,
        context.subject_repository,
        collector_factory,
        generators,  # type: ignore
        progress_cycle_output_port,
        storage,
    )


def new_cli_controller(config: Config):
    context = AppContext(config)
    inferential_analysis_usecase_factory = new_inferential_analysis_usecase_factory(
        context
    )
    inferential_controller = InferentialStatisticsCLIController(
        context.inferential_result_repository, inferential_analysis_usecase_factory
    )

    spaguetty_controller = PlotCLIController(
        new_spaghetti_plot_usecase_factory(context)
    )
    controller = CLIController(inferential_controller, spaguetty_controller)
    return controller

from adapter.presenter import progress_presenter
from adapter.presenter.progress_presenter import ProgressPresenter
from application.service.collector import collector_factory
from bootstrap.config import Config
from application.port.input.inferential_statistics_input_port import (
    InferentialStatisticsInputPort,
)
from application.usecase.run_inferential_analysis_usecase import (
    RunInferentialAnalysisUseCase,
)
from bootstrap.inferential_statistics_factory import InferentialUsecaseFactory
from bootstrap.plot_data_usecase_factory import PlotDataUsecaseFactory
from domain.value.condition import Condition, Position, CoolingMode

from typing import Callable, List

from application.port.output.inferential_statistics_output_port import (
    InferentialResultOutputPort,
)
from application.port.output.progress_output_port import (
    ProgressLifeCycleOutputPort,
)

from application.port.output.progress_output_port import ProgressAdvanceOutputPort
from infra.calculator.inferential import calculator_factory
from infra.calculator.inferential.calculator_factory import CalculatorFactory
from infra.calculator.inferential.paired_t_test_calculator import PairedTTestCalculator
from infra.calculator.inferential.wilcoxon_calculator import WilcoxonCalculator
from infra.graph.error_bar_plot_generator import ErrorBarPlotGenerator
from infra.post_processor.holm_post_processor import HolmPostProcessor
from domain.analysis.inferential.post_processor import PostProcessor
from adapter.controller.cli_controller import CLIController
from adapter.controller.inferential_analysis_cli_controller import (
    InferentialStatisticsCLIController,
)
from application.service.collector.collector_factory_impl import CollectorFactoryImpl, new_collector_factory
from infra.calculator.inferential.friedman_calculator import FriedmanCalculator
from bootstrap.context import AppContext
from infra.strage.file_graph_storage import FileGraphStorage
from application.usecase.plot_data_usecase import PlotDataUseCase
from infra.graph.spaghetti_plot_generator import SpaghettiPlotGenerator
from adapter.controller.plot_cli_controller import PlotCLIController
from infra.graph.box_plot_generator import BoxPlotGenerator
from infra.value_filter.iqr_filter import IQRFilter
from infra.value_filter.name_filter import NameFilter



def new_cli_controller(config: Config):
    context = AppContext(config)
    progress_presenter = ProgressPresenter()
    value_filters = [NameFilter(config.sensored),IQRFilter(config.iqr_factor)]
    collector_factory = new_collector_factory(context,progress_presenter)
    calculator_factory = CalculatorFactory()
    inferential_controller = InferentialStatisticsCLIController(
        InferentialUsecaseFactory(collector_factory,value_filters,calculator_factory)
    )

    generators = [SpaghettiPlotGenerator(),BoxPlotGenerator(config.iqr_factor),ErrorBarPlotGenerator()]
    plot_controller = PlotCLIController(
        PlotDataUsecaseFactory(context,collector_factory,value_filters,generators)
    )
    controller = CLIController(context,inferential_controller, plot_controller)
    return controller

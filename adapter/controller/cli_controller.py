from adapter.controller.inferential_analysis_cli_controller import (
    InferentialStatisticsCLIController,
)
from adapter.controller.plot_cli_controller import PlotCLIController
from bootstrap.context import AppContext


class CLIController:
    def __init__(
        self,
        context:AppContext,
        inferential_analysis_cli_controller: InferentialStatisticsCLIController,
        plot_cli_controller: PlotCLIController,
    ) -> None:
        self.context = context
        self.inferential_analysis_cli_controller = inferential_analysis_cli_controller
        self.plot_cli_controller = plot_cli_controller

    def handle(self, input_line: str):
        split_result = input_line.split()
        if len(split_result) == 0:
            raise ValueError("Command not found")

        command = split_result[0]
        if command == "inferential":
            self.inferential_analysis_cli_controller.handle(self.context,input_line[len(command) :])
        elif command == "plot":
            self.plot_cli_controller.handle(input_line[len(command) :])

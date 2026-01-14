from adapter.controller.inferential_analysis_cli_controller import (
    InferentialStatisticsCLIController,
)


class CLIController:
    def __init__(
        self, inferential_analysis_cli_controller: InferentialStatisticsCLIController
    ) -> None:
        self.inferential_analysis_cli_controller = inferential_analysis_cli_controller

    def handle(self, input_line: str):
        split_result = input_line.split()
        if len(split_result) == 0:
            raise ValueError("Command not found")

        command = split_result[0]
        if command == "inferential":
            self.inferential_analysis_cli_controller.handle(input_line[len(command) :])

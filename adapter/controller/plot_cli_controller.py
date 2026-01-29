from adapter.parser import plot_args_from_json
from bootstrap.plot_data_usecase_factory import PlotDataUsecaseFactory


class PlotCLIController:
    def __init__(
        self,
        usecase_factory: PlotDataUsecaseFactory
    ):
        self.usecase_factory = usecase_factory

    def handle(self, input_line: str):
        args = plot_args_from_json(input_line)
        usecase = self.usecase_factory.create_plot_usecase(args.value_type,args.graph_type,args.conditions)

        usecase.execute(args.title,args.option)


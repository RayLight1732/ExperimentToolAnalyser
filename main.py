from typing import Optional
import sys
from bootstrap.config import load_config
from bootstrap.wire import new_cli_controller
from application.model.value_type import ValueType
from application.model.graph_type import GraphType


def run_all(controller, filter):
    controller.handle(f"inferential {ValueType.PEAK_FMS.name} {filter}")
    controller.handle(f"inferential {ValueType.AVERAGE_COP_SPEED.name} {filter}")
    controller.handle(f"inferential {ValueType.SSQ_DISORIENTATION.name} {filter}")
    controller.handle(f"inferential {ValueType.SSQ_NAUSEA.name} {filter}")
    controller.handle(f"inferential {ValueType.SSQ_OCULOMOTOR.name} {filter}")
    controller.handle(f"inferential {ValueType.SSQ_TOTAL.name} {filter}")
    graph_type = GraphType.BOX_PLOT
    controller.handle(f"plot {ValueType.PEAK_FMS.name} {filter} {graph_type}")
    controller.handle(f"plot {ValueType.AVERAGE_COP_SPEED.name} {filter} {graph_type}")
    controller.handle(f"plot {ValueType.SSQ_DISORIENTATION.name} {filter} {graph_type}")
    controller.handle(f"plot {ValueType.SSQ_NAUSEA.name} {filter} {graph_type}")
    controller.handle(f"plot {ValueType.SSQ_OCULOMOTOR.name} {filter} {graph_type}")
    controller.handle(f"plot {ValueType.SSQ_TOTAL.name} {filter} {graph_type}")


def main(config_path):
    config = load_config(config_path)
    controller = new_cli_controller(config)
    run_all(controller, False)
    run_all(controller, True)


if __name__ == "__main__":
    config: Optional[str] = None

    if len(sys.argv) > 1:
        config = sys.argv[1]

    main(config)

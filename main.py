from typing import Optional
import sys
from bootstrap.config import load_config
from bootstrap.wire import new_cli_controller
from application.model.value_type import ValueType


def run_all(controller, filter):
    controller.handle(f"inferential {ValueType.PEAK_FMS.name} {filter}")
    controller.handle(f"inferential {ValueType.AVERAGE_COP_SPEED.name} {filter}")
    controller.handle(f"inferential {ValueType.SSQ_DISORIENTATION.name} {filter}")
    controller.handle(f"inferential {ValueType.SSQ_NAUSEA.name} {filter}")
    controller.handle(f"inferential {ValueType.SSQ_OCULOMOTOR.name} {filter}")
    controller.handle(f"inferential {ValueType.SSQ_TOTAL.name} {filter}")

    controller.handle(f"spaghetti {ValueType.PEAK_FMS.name} {filter}")
    controller.handle(f"spaghetti {ValueType.AVERAGE_COP_SPEED.name} {filter}")
    controller.handle(f"spaghetti {ValueType.SSQ_DISORIENTATION.name} {filter}")
    controller.handle(f"spaghetti {ValueType.SSQ_NAUSEA.name} {filter}")
    controller.handle(f"spaghetti {ValueType.SSQ_OCULOMOTOR.name} {filter}")
    controller.handle(f"spaghetti {ValueType.SSQ_TOTAL.name} {filter}")


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

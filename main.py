from typing import Optional
import sys
from bootstrap.config import load_config
from bootstrap.wire import new_cli_controller
from application.dto.value_type import ValueType


def main(config_path):
    config = load_config(config_path)
    controller = new_cli_controller(config)
    controller.handle(f"inferential {ValueType.PEAK_FMS.name}")
    controller.handle(f"inferential {ValueType.AVERAGE_COP_SPEED.name}")
    controller.handle(f"inferential {ValueType.SSQ_DISORIENTATION.name}")
    controller.handle(f"inferential {ValueType.SSQ_NAUSEA.name}")
    controller.handle(f"inferential {ValueType.SSQ_OCULOMOTOR.name}")
    controller.handle(f"inferential {ValueType.SSQ_TOTAL.name}")


if __name__ == "__main__":
    config: Optional[str] = None

    if len(sys.argv) > 1:
        config = sys.argv[1]

    main(config)

import sys
from bootstrap.config import load_config
from typing import Optional
from bootstrap.wire import (
    new_app_context,
    new_statistics_controller,
)
from presentation.presenter.collect_value_presenter import CollectValuePresenter
from presentation.presenter.mean_and_se_presenter import MeanAndSePresenter
from presentation.presenter.paired_t_test_presenter import PairedTTestPresenter
from application.dto.value_type import ValueType


def main(config_path: Optional[str] = None) -> None:
    config = load_config(config_path)
    app_context = new_app_context(config)
    collect_value_presenter = CollectValuePresenter()
    mean_and_se_presenter = MeanAndSePresenter()
    paired_t_test_presenter = PairedTTestPresenter()
    controller = new_statistics_controller(
        app_context,
        mean_and_se_presenter,
        paired_t_test_presenter,
        collect_value_presenter,
    )

    controller.calculate_mean_and_se(
        [
            ValueType.AVERAGE_COP_SPEED,
        ]
    )
    # controller.run_paired_t_test_with_holm(
    #     [
    #         ValueType.AVERAGE_COP_SPEED,
    #     ]
    # )


if __name__ == "__main__":
    config: Optional[str] = None

    if len(sys.argv) > 1:
        config = sys.argv[1]

    main(config)

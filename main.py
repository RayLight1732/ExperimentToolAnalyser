import sys
from bootstrap.config import load_config
from typing import Optional, Dict
from bootstrap.wire import (
    new_app_context,
    new_statistics_controller,
)
from presentation.presenter.collect_value_presenter import CollectValuePresenter
from presentation.presenter.mean_and_se_presenter import MeanAndSePresenter
from presentation.presenter.paired_t_test_presenter import PairedTTestPresenter
from application.dto.value_type import ValueType
from application.dto.filter_parameter import FilterParameter
from application.dto.filter_type import FilterType
from collections import defaultdict


def store_mean_and_se(results_dict, type, result):
    results_dict[type]["mean_and_se"] = result


def store_t_test_result(results_dict, type, result):
    results_dict[type]["t_test"] = result


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

    results: Dict[ValueType, Dict] = defaultdict(lambda: {})

    mean_and_se_presenter.on_complete_callback = lambda type, result: store_mean_and_se(
        results, type, result
    )
    paired_t_test_presenter.on_complete_callback = (
        lambda type, result: store_t_test_result(results, type, result)
    )

    controller.calculate_mean_and_se(
        [
            ValueType.AVERAGE_COP_SPEED,
            ValueType.SSQ_NAUSEA,
            ValueType.SSQ_DISORIENTATION,
            ValueType.SSQ_OCULOMOTOR,
            ValueType.SSQ_TOTAL,
            ValueType.PEAK_FMS,
        ]
    )
    controller.run_paired_t_test_with_holm(
        [
            ValueType.AVERAGE_COP_SPEED,
            ValueType.SSQ_NAUSEA,
            ValueType.SSQ_DISORIENTATION,
            ValueType.SSQ_OCULOMOTOR,
            ValueType.SSQ_TOTAL,
            ValueType.PEAK_FMS,
        ]
    )

    for type, d in results.items():
        controller.save_calculation_result(f"{type}.csv", d["mean_and_se"], d["t_test"])

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

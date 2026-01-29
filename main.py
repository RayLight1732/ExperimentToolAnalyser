import json
from typing import List, Optional
import sys
from adapter.controller.cli_controller import CLIController
from application.model.graph_options import GraphOption
from bootstrap.config import load_config
from bootstrap.wire import new_cli_controller
from application.model.value_type import ValueType
from application.model.graph_type import GraphType
from domain.analysis.inferential.options.two_sample_test_option import (
    TwoSampleTestOption,
)
from domain.analysis.inferential.result.comparison import Comparison
from domain.analysis.inferential.test_type import TestType
from domain.value.condition import Condition, CoolingMode, Position


def condition_to_dict(c: Condition | None) -> dict | None:
    if c is None:
        return None

    data = {"mode": c.mode.name}
    if c.position is not None:
        data["position"] = c.position.name

    return data


def comparison_to_dict(cmp: Comparison) -> dict:
    return {
        "left": condition_to_dict(cmp.left),
        "right": condition_to_dict(cmp.right),
    }


def two_sample_option_to_dict(opt: TwoSampleTestOption) -> dict:
    return {"comparisons": [comparison_to_dict(cmp) for cmp in opt.comparisons]}


def test_args_to_json(
    file_name: str,
    value_type: ValueType,
    test_type: TestType,
    conditions: List[Condition],
    option: dict,
) -> str:
    result_dict = {}
    result_dict["file_name"] = file_name
    result_dict["value_type"] = value_type.name
    result_dict["test_type"] = test_type.name
    result_dict["conditions"] = [
        condition_to_dict(condition) for condition in conditions
    ]
    result_dict["option"] = option
    return json.dumps(result_dict, ensure_ascii=False, indent=2)

def graph_option_to_dict(option:GraphOption):
    result_dict = {}
    result_dict["x_label"] = option.x_label
    result_dict["y_label"] = option.y_label
    result_dict["color_theme"] = option.color_theme
    result_dict["width"] = option.width
    result_dict["height"] = option.height
    #TODO custom option
    return result_dict
    


def graph_args_to_json(
    file_name: str,
    value_type: ValueType,
    graph_type:GraphType,
    conditions: List[Condition],
    option: GraphOption
)->str:
    result_dict = {}
    result_dict["title"] = file_name
    result_dict["value_type"] = value_type.name
    result_dict["graph_type"] = graph_type.name
    result_dict["conditions"] = [
        condition_to_dict(condition) for condition in conditions
    ]
    result_dict["option"] = graph_option_to_dict(option)
    return json.dumps(result_dict, ensure_ascii=False, indent=2)


def run_all(controller: CLIController, filter):
    value_type = ValueType.PEAK_FMS
    test_type = TestType.WILCOXON_TEST
    graph_type = GraphType.BOX_PLOT
    required = {
        Condition(CoolingMode.ALWAYS_STRONG,Position.CAROTID),
        Condition(CoolingMode.ALWAYS, Position.CAROTID),
        Condition(CoolingMode.PERIODIC, Position.CAROTID),
        Condition(CoolingMode.SICK_SCENE_ONLY, Position.CAROTID),
        Condition(CoolingMode.NONE),
    }
    option = TwoSampleTestOption(
        [
            Comparison(
                Condition(CoolingMode.PERIODIC, Position.CAROTID),
                Condition(CoolingMode.NONE),
            ),
            Comparison(
                Condition(CoolingMode.ALWAYS_STRONG,Position.CAROTID),
                Condition(CoolingMode.NONE)
            ),
            Comparison(
                Condition(CoolingMode.ALWAYS,Position.CAROTID),
                Condition(CoolingMode.NONE)
            ),
        ]
    )
    option = TwoSampleTestOption([])
    size = len(required) if len(option.comparisons) == 0 else len(option.comparisons)

    graph_option = GraphOption(
        x_label="組み合わせ",
        y_label=value_type.name,
    )
    title = f"Peak FMS ({size} conditions)"
    controller.handle(
         f"inferential {test_args_to_json(title,value_type,test_type,required,two_sample_option_to_dict(option))}"
    )
    controller.handle(
        f"plot {graph_args_to_json(title,value_type,graph_type,required,graph_option)}"
    )

    value_type = ValueType.SSQ_TOTAL
    title = f"Delta SSQ ({size} conditions)"
    controller.handle(
         f"inferential {test_args_to_json(title,value_type,test_type,required,two_sample_option_to_dict(option))}"
    )

    controller.handle(
        f"plot {graph_args_to_json(title,value_type,graph_type,required,graph_option)}"
    )

    value_type = ValueType.AVERAGE_COP_SPEED
    
    title = f"Average CoP Speed ({size} conditions)"
    controller.handle(
         f"inferential {test_args_to_json(title,value_type,test_type,required,two_sample_option_to_dict(option))}"
    )

    controller.handle(
        f"plot {graph_args_to_json(title,value_type,graph_type,required,graph_option)}"
    )
 

def main(config_path):
    config = load_config(config_path)
    controller = new_cli_controller(config)
    run_all(controller, False)
    # run_all(controller, True)


if __name__ == "__main__":
    config: Optional[str] = None

    if len(sys.argv) > 1:
        config = sys.argv[1]

    main(config)

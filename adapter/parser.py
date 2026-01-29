from application.model.graph_options import GraphOption
from domain.analysis.inferential.options.two_sample_test_option import (
    TwoSampleTestOption,
)
from domain.analysis.inferential.result.comparison import Comparison
from domain.analysis.inferential.test_type import TestType
from domain.value.condition import Condition, CoolingMode, Position
from application.model.value_type import ValueType
from application.model.graph_type import GraphType
from dataclasses import dataclass
from typing import List, Optional, Tuple
import json


def parse_value_type_str(input_str: str) -> ValueType:
    return ValueType[input_str.strip().upper()]


def parse_bool(input_str: str) -> bool:
    return input_str.strip().lower() == "true"


def parse_graph_type(input_str: str) -> bool:
    return GraphType[input_str.strip().upper()]


def condition_from_json(data: dict | None) -> Optional[Condition]:
    if data is None:
        return None

    try:
        mode = CoolingMode[data["mode"]]
    except KeyError:
        raise ValueError(f"不明な CoolingMode: {data.get('mode')}")

    position = None
    if "position" in data:
        try:
            position = Position[data["position"]]
        except KeyError:
            raise ValueError(f"不明な Position: {data.get('position')}")

    return Condition(mode=mode, position=position)


def comparison_from_json(data: dict) -> Comparison:
    left = condition_from_json(data.get("left"))
    right = condition_from_json(data.get("right"))
    return Comparison(left=left, right=right)


def two_sample_test_option_from_json(data: dict) -> TwoSampleTestOption:
    return TwoSampleTestOption(
        [comparison_from_json(comparison) for comparison in data["comparisons"]]
    )


def test_args_from_json(text: str) -> Tuple[TestType, List[Condition], str, str]:
    data = json.loads(text)

    # TestType
    try:
        test_type = TestType[data["test_type"]]
    except KeyError:
        raise ValueError(f"不明な TestType: {data.get('test_type')}")

    try:
        value_type = ValueType[data["value_type"]]
    except KeyError:
        raise ValueError(f"不明な ValueType: {data.get('value_type')}")

    # Conditions
    conditions = set()
    for i, c in enumerate(data["conditions"]):
        conditions.add(condition_from_json(c))

    file_name = data["file_name"]
    option = data["option"]

    return test_type, value_type, conditions, file_name, option


# TODO DTO専用の場所に移動
@dataclass(frozen=True)
class PlotArgs:
    graph_type: GraphType
    value_type: ValueType
    conditions: List[Condition]
    title: str
    option: GraphOption


def graph_option_from_json(data: dict)->GraphOption:
    x_label = data["x_label"]
    y_label = data["y_label"]
    color_theme = data.get("color_theme","default")
    width = data.get("width",800)
    height = data.get("height",600)
    # TODO custom option
    return GraphOption(width,height,x_label,y_label,color_theme)
    


def plot_args_from_json(text: str) -> PlotArgs:
    data = json.loads(text)
    title = data["title"]
    try:
        graph_type = GraphType[data["graph_type"]]
    except KeyError:
        raise ValueError(f"不明な GraphType: {data.get(' graph_type')}")

    try:
        value_type = ValueType[data["value_type"]]
    except KeyError:
        raise ValueError(f"不明な ValueType: {data.get('value_type')}")


    # Conditions
    conditions = set()
    for i, c in enumerate(data["conditions"]):
        conditions.add(condition_from_json(c))

    option = graph_option_from_json(data["option"])
    return PlotArgs(graph_type,value_type, conditions, title, option)

from typing import Type
from application.model.graph_type import GraphType
from application.model.graph_options import GraphOptions
from application.port.output.graph_generator import GraphGenerator
import matplotlib.pyplot as plt
from typing import cast, Optional, List, Dict
import io
from domain.value.grouped_value import GroupedValue
from domain.value.subject_data import SubjectData
from domain.value.condition import Condition
from dataclasses import dataclass
from collections import defaultdict
import japanize_matplotlib


class SpaghettiPlotGenerator(GraphGenerator):

    def generate(self, title: str, data: GroupedValue, option: GraphOptions) -> bytes:
        assert option is not None
        series_list = to_spaghetti_series(data)

        only_mode = Condition.all_same_position(data.value.keys())
        if only_mode:
            x_label_factory = lambda c: c.mode.display_name
        else:
            x_label_factory = str

        plt.figure(figsize=(7, 5))
        for series in series_list:
            plt.plot(
                [x_label_factory(x_value) for x_value in series.x_values],
                series.y_values,
                marker=series.marker,
                alpha=0.6,
            )

        plt.xlabel(option.x_label)
        plt.ylabel(option.y_label)
        plt.title(title)
        ax = plt.gca()
        ax.text(
            0.98,
            0.98,
            f"N = {len(series_list)}",
            transform=ax.transAxes,  # ← 0〜1 の座標系
            ha="right",
            va="top",
            fontsize=11,
            alpha=0.8,
        )

        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        return buf.read()

    def supported_type(self) -> GraphType:
        """サポートするグラフタイプを返す"""
        return GraphType.SPAGHETTI


@dataclass
class SpaghettiDataSeries:
    """スパゲッティグラフのデータ系列"""

    name: str
    x_values: List[Condition]
    y_values: List[float]
    line_style: str = "-"  # solid, dashed, dotted
    marker: str = "o"
    color: Optional[str] = None


def to_spaghetti_series(
    grouped: GroupedValue,
) -> List[SpaghettiDataSeries]:
    """
    GroupedValue (condition -> subject -> value)
    → List[SpaghettiDataSeries] (1 subject = 1 line)
    """

    conditions = grouped.value.keys()
    condition_order = sorted(conditions, key=lambda value: str(value))

    # subject -> {condition -> value}
    subject_map: Dict[SubjectData, Dict[Condition, float]] = defaultdict(dict)

    # 転置（condition→subject を subject→condition に）
    for condition, subject_dict in grouped.value.items():
        for subject, value in subject_dict.items():
            subject_map[subject][condition] = value

    series_list: List[SpaghettiDataSeries] = []

    for subject, cond_values in subject_map.items():
        x_vals: List[Condition] = []
        y_vals: List[float] = []

        for cond in condition_order:
            if cond in cond_values:
                x_vals.append(cond)
                y_vals.append(cond_values[cond])

        series_list.append(
            SpaghettiDataSeries(
                name=subject.name,
                x_values=x_vals,
                y_values=y_vals,
            )
        )

    return series_list

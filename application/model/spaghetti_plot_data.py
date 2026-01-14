from dataclasses import dataclass, field
from typing import List
from .graph_data import GraphData
from .graph_type import GraphType
from typing import Optional, List, Dict
from domain.value.grouped_value import GroupedValue
from domain.value.condition import Condition
from collections import defaultdict
from domain.value.subject_data import SubjectData


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
    condition_order: List[Condition],
) -> List[SpaghettiDataSeries]:
    """
    GroupedValue (condition -> subject -> value)
    → List[SpaghettiDataSeries] (1 subject = 1 line)
    """

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


@dataclass
class SpaghettiPlotData(GraphData):
    """スパゲッティプロット専用のデータモデル"""

    series: List[SpaghettiDataSeries] = field(default_factory=list)
    x_label: str = "X"
    y_label: str = "Y"
    show_grid: bool = False

    def __post_init__(self):
        if self.type != GraphType.SPAGHETTI:
            raise ValueError("LineGraphData must have type=GraphType.LINE")

    def to_dict(self):
        base = super().to_dict()
        base.update(
            {
                "series": [
                    {
                        "name": s.name,
                        "x_values": s.x_values,
                        "y_values": s.y_values,
                        "line_style": s.line_style,
                        "marker": s.marker,
                        "color": s.color,
                    }
                    for s in self.series
                ],
                "x_label": self.x_label,
                "y_label": self.y_label,
                "show_grid": self.show_grid,
            }
        )
        return base

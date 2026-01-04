from typing import Any, Dict, List
import matplotlib.pyplot as plt
import japanize_matplotlib  # type: ignore[import-untyped]
from application.dto.mean_and_se import MeanAndSEByCondition
from domain.value_object.condition import Condition
from application.port.output.calculator.calculate_mean_and_se_output_port import (
    CalculateMeanAndSEOutputPort,
)
from application.dto.value_type import ValueType


class MeanAndSePresenter(CalculateMeanAndSEOutputPort):
    def __init__(self, on_complete_callback=None):
        self.results = {}
        self.on_complete_callback = on_complete_callback

    def on_start(self, value_type: ValueType) -> None:
        pass

    def on_complete(
        self,
        value_type: ValueType,
        result: MeanAndSEByCondition,
    ) -> None:
        self._plot_mean_and_se(
            result,
            title=f"{value_type} 平均値 ± 標準誤差",
        )
        if self.on_complete_callback is not None:
            self.on_complete_callback(value_type, result)

    def on_error(
        self,
        value_type: ValueType,
        error: Exception,
    ) -> None:
        pass

    def _plot_mean_and_se(
        self,
        values: MeanAndSEByCondition,
        *,
        condition_order: List[Condition] | None = None,
        title: str | None = None,
        ylabel: str = "値",
        xlabel: str = "条件",
    ) -> None:
        """
        Conditionごとの平均値 ± 標準誤差をプロットする
        - y軸は0始まり
        - 日本語フォント対応
        """

        if not values:
            raise ValueError("No values to plot")

        # ---------- プロット順 ----------
        conditions = condition_order if condition_order else list(values.values.keys())

        means = [values.values[c].mean for c in conditions]
        ses = [values.values[c].standard_error for c in conditions]
        labels = [str(c) for c in conditions]

        x = range(len(conditions))

        # ---------- 描画 ----------
        plt.figure()
        plt.errorbar(x, means, yerr=ses, fmt="o", capsize=5)

        plt.xticks(x, labels)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

        # y軸を0始まりにする
        plt.ylim(bottom=0)

        if title:
            plt.title(title)

        plt.tight_layout()
        plt.show()

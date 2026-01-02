import sys
from typing import Optional, Dict, List
from bootstrap.wire import new_completed_subject_find_usecase, new_statistics_usecase
from bootstrap.config import load_config
from domain.value_object.condition import Condition
from domain.analysis.result.mean_and_se import MeanAndSE
from domain.entity.subject import Subject
from usecase.service.operation_registory import ValueType, CalculationType
import matplotlib.pyplot as plt
from domain.analysis.result.mean_and_se import MeanAndSEByCondition
import japanize_matplotlib  # type: ignore[import-untyped]
from bootstrap.config import Config


def plot_mean_and_se(
    values: Dict[Condition, MeanAndSE],
    *,
    condition_order: List[Condition] | None = None,
    title: str | None = None,
    ylabel: str = "値",
    xlabel: str = "条件"
) -> None:
    """
    Conditionごとの平均値 ± 標準誤差をプロットする
    - y軸は0始まり
    - 日本語フォント対応
    """

    if not values:
        raise ValueError("No values to plot")

    # ---------- プロット順 ----------
    conditions = condition_order if condition_order else list(values.keys())

    means = [values[c].mean for c in conditions]
    ses = [values[c].standard_error for c in conditions]
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


def main(config_path: Optional[str] = None) -> None:
    config = load_config(config_path)
    usecase = new_completed_subject_find_usecase(config)
    subjects = usecase.execute()
    for subject in subjects:
        print(subject.data.name)
    statistics_usecase = new_statistics_usecase(config)
    result: MeanAndSEByCondition = statistics_usecase.execute(
        subjects,
        value_type=ValueType.FMS,
        calculation_type=CalculationType.MEAN_AND_SE,
    )
    plot_mean_and_se(result.values, title="FMS Mean and SE")


if __name__ == "__main__":
    config: Optional[str] = None

    if len(sys.argv) > 1:
        config = sys.argv[1]

    main(config)

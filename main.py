import sys
from typing import Optional,Dict, List
from bootstrap.wire import new_completed_subject_find_usecase,new_mean_peak_fms_calculate_usecase,new_peak_fms_anova_usecase,new_mean_and_se_fms_usecase, new_peak_fms_paired_t_test_with_holm_calculator
from bootstrap.config import load_config
from domain.value_object.condition import Condition
from domain.analysis.result.mean_and_se import MeanAndSE
import matplotlib.pyplot as plt
import japanize_matplotlib # type: ignore[import-untyped]

def mean_peak_fms(config,subjects):
    mean_peak_fms_calculate_usecase = new_mean_peak_fms_calculate_usecase(config)

    for condition,value in mean_peak_fms_calculate_usecase.execute(subjects).values.items():
        print(condition,value)
    
def peak_fms_anova(config,subjects):
    usecase = new_peak_fms_anova_usecase(config)
    print(usecase.execute(subjects))

def peak_fms_paired_t_and_holm(config,subjects):
    usecase = new_peak_fms_paired_t_test_with_holm_calculator(config)
    result = usecase.execute(subjects)
    for condition_tuple,value in result.values.items():
        print(condition_tuple[0].mode.display_name,condition_tuple[1].mode.display_name,value)


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
    plt.errorbar(
        x,
        means,
        yerr=ses,
        fmt="o",
        capsize=5
    )

    plt.xticks(x, labels)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    # y軸を0始まりにする
    plt.ylim(bottom=0)

    if title:
        plt.title(title)

    plt.tight_layout()
    plt.show()

def mean_and_se_peak_fms(config,subjects):
    usecase = new_mean_and_se_fms_usecase(config)

    # for condition,value in usecase.execute(subjects).items():
    #     print(condition,value)
    plot_mean_and_se(usecase.execute(subjects))
    

def main(config_path: Optional[str] = None) -> None:
    config= load_config(config_path)
    usecase = new_completed_subject_find_usecase(config)
    subjects = usecase.execute()
    for subject in subjects:
        print(subject.data.name)
    peak_fms_paired_t_and_holm(config,subjects)



if __name__ == "__main__":
    config: Optional[str] = None

    if len(sys.argv) > 1:
        config = sys.argv[1]

    main(config)
from application.model.graph_type import GraphType
from application.model.graph_options import GraphOption
from application.port.output.graph_generator import GraphGenerator
from domain.value.grouped_value import GroupedValue
from domain.value.condition import Condition
import numpy as np
import matplotlib.pyplot as plt
import io
import japanize_matplotlib


class ErrorBarPlotGenerator(GraphGenerator):

    def generate(self, title: str, data: GroupedValue, option: GraphOption) -> bytes:
        assert option is not None

        # condition の並び順を安定させる
        conditions = sorted(data.value.keys(), key=lambda c: str(c))

        # 各 condition ごとの値リストを作成
        value_length = -1
        x_labels = []
        means = []
        sems = []
    
        only_mode = Condition.all_same_position(data.value.keys())
        if only_mode:
            label_factory = lambda c: c.mode.display_name
        else:
            label_factory = str

        for condition in conditions:
            subject_dict = data.value[condition]
            values = list(subject_dict.values())

            last_value_length = value_length
            value_length = len(values)
            if last_value_length != -1 and last_value_length != value_length:
                raise Exception("value length is not equal to the other")

            if value_length  == 0:
                continue
            np_values = np.array(values)
            means.append(np_values.mean())
            sems.append(np_values.std(ddof=1) / np.sqrt(len(np_values)))
            x_labels.append(label_factory(condition))

        # 描画
        plt.figure(figsize=(7, 5))
        plt.bar(
            x_labels,
            means,
            yerr=sems,
            capsize=5,
            error_kw=dict(ecolor='black', lw=1.5)
        )
        plt.ylim(0, None)
        plt.xlabel(option.x_label)
        plt.ylabel(option.y_label)
        plt.title(title)

        ax = plt.gca()
        ax.text(
            0.98,
            0.98,
            f"N = {value_length}",
            transform=ax.transAxes,
            ha="right",
            va="top",
            fontsize=11,
            alpha=0.8,
        )

        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format="png")
        plt.close()
        buf.seek(0)
        return buf.read()

    def supported_type(self) -> GraphType:
        """サポートするグラフタイプを返す"""
        return GraphType.ERROR_BAR

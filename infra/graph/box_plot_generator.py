from application.model.graph_type import GraphType
from application.model.graph_options import GraphOptions
from application.port.output.graph_generator import GraphGenerator
from domain.value.grouped_value import GroupedValue
from domain.value.condition import Condition

import matplotlib.pyplot as plt
import io
import japanize_matplotlib


class BoxPlotGenerator(GraphGenerator):

    def generate(self, title: str, data: GroupedValue, option: GraphOptions) -> bytes:
        assert option is not None

        # condition の並び順を安定させる
        conditions = sorted(data.value.keys(), key=lambda c: str(c))

        # 各 condition ごとの値リストを作成
        box_values = []
        x_labels = []

        only_mode = Condition.all_same_position(data.value.keys())
        if only_mode:
            label_factory = lambda c: c.mode.display_name
        else:
            label_factory = str

        for condition in conditions:
            subject_dict = data.value[condition]
            values = list(subject_dict.values())

            if len(values) == 0:
                continue

            box_values.append(values)
            x_labels.append(label_factory(condition))

        # 描画
        plt.figure(figsize=(7, 5))
        plt.boxplot(
            box_values,
            labels=x_labels,
            showfliers=True,   # 外れ値を表示
            patch_artist=True # 箱を塗りつぶせるように
        )

        plt.xlabel(option.x_label)
        plt.ylabel(option.y_label)
        plt.title(title)

        ax = plt.gca()
        ax.text(
            0.98,
            0.98,
            f"N = {len(box_values[0]) }",
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
        return GraphType.BOX_PLOT

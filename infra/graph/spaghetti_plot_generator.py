from typing import Type
from domain.graph.graph_data import GraphData
from domain.graph.graph_type import GraphType
from application.model.graph_options import GraphOptions
from application.port.output.graph_generator import GraphGenerator
from domain.graph.spaghetti_plot_data import SpaghettiPlotData


class SpaghettiPlotGenerator(GraphGenerator):
    """グラフ生成の抽象インターフェース"""

    def generate(self, data: GraphData, option: GraphOptions) -> bytes:
        """
        グラフを生成してバイナリデータを返す

        Args:
            data: グラフデータ（具体的な型は各実装で異なる）

        Returns:
            生成されたグラフの画像データ
        """
        pass

    def supported_type(self) -> GraphType:
        """サポートするグラフタイプを返す"""
        return GraphType.SPAGHETTI

    def expected_data_type(self) -> Type[GraphData]:
        """期待するデータ型を返す"""
        return SpaghettiPlotData

from typing import List, Dict
from application.model.graph_options import GraphOptions
from application.port.output.graph_storage_output_port import GraphStorageOutputPort
from application.port.output.graph_generator import GraphGenerator
from application.model.graph_type import GraphType
from application.model.graph_data import GraphData


class CreateGraphUseCase:
    """グラフ作成のユースケース"""

    def __init__(
        self, output_port: GraphStorageOutputPort, generators: List[GraphGenerator]
    ):
        self.output_port = output_port
        self._generators: Dict[GraphType, GraphGenerator] = {
            gen.supported_type(): gen for gen in generators
        }

    def execute(self, name: str, graph_data: GraphData, option: GraphOptions):
        """
        グラフを生成して保存する

        Args:
            graph_data: グラフデータ（具体的な型）

        Returns:
            生成されたグラフの画像データ

        Raises:
            ValueError: サポートされていないグラフタイプまたは型不一致の場合
        """
        # グラフタイプの検証
        if graph_data.type not in self._generators:
            raise ValueError(f"Unsupported graph type: {graph_data.type}")

        generator = self._generators[graph_data.type]

        # データ型の検証
        expected_type = generator.expected_data_type()
        if not isinstance(graph_data, expected_type):
            raise ValueError(
                f"Invalid data type for {graph_data.type}. "
                f"Expected {expected_type.__name__}, got {type(graph_data).__name__}"
            )

        # グラフ生成
        image_data = generator.generate(graph_data, option)

        # 保存
        self.output_port.save(name, image_data)

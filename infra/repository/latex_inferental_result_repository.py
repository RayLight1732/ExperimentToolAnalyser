from cProfile import label
from domain.analysis.inferential.result.comparison import Comparison
from domain.value.condition import Condition
from domain.value.laveled_value import LaveledValues
from domain.repository.inferential_result_repository import (
    InferentialResultRepository as IInferentialResultRepository,
)
from domain.analysis.inferential.result.inferential_result_history import (
    InferentialResultHistory,
)
from domain.analysis.inferential.result.inferential_result import InferentialResult
from infra.file_system.file_system import FileSystem
from typing import Generator, List, Any
from infra.file_system.path_resolver import PathResolver
import unicodedata

class LatexInferentialResultRepository(IInferentialResultRepository):
    def __init__(self, path_resolver: PathResolver, file_system: FileSystem,num_format:str=">7.4f") -> None:
        self.path_resolver = path_resolver
        self.file_system = file_system
        self.num_format = num_format

    def save(self, name: str, result: InferentialResultHistory):
        self.file_system.save_text(
            self.path_resolver.save_path(name+".txt"),
            self._generate_inferential_result_history(result),
        )

    def _generate_inferential_result_history(
        self, result: InferentialResultHistory
    ) -> Generator[str, None, None]:

        sorted_items = sorted(
            result.original.comparisons.items(),
            key=lambda pair: pair[1].p_value
        )

        conditions = {
            c
            for comparison, _ in sorted_items
            for c in (comparison.left, comparison.right)
            if c is not None
        }
        show_position = not Condition.all_same_position(conditions)

        labels = {
            comparison: comparison.to_label(show_position)
            for comparison, _ in sorted_items
        }
        label_width = max(get_count_as_half_width(label) for label in labels.values())+3

        yield " & ".join(
            ["Comparison", result.original.method]
            + [p.method for p in result.post_process]
        ) + r" \\ \hline"

        for comparison, _ in sorted_items:
            yield self._generate_result_by_comparison(
                result,
                comparison,
                text_align(labels[comparison],label_width),
            )

    def _generate_result_by_comparison(
        self,
        result: InferentialResultHistory,
        comparison: Comparison,
        label: str
    ) -> str:
        values: List[str] = []

        values.append(f"{result.original.comparisons[comparison].p_value:{self.num_format}}")
        for post_process in result.post_process:
            values.append(
                f"{post_process.comparisons[comparison].p_value:{self.num_format}}"
            )

        return (
            label
            + " & "
            + " & ".join(values)
            + r" \\ \hline"
        )
    
def get_count_as_half_width(text):
    count = 0

    for char in text:
        if unicodedata.east_asian_width(char) in 'FWA':
            count += 2
        else:
            count += 1

    return count

def text_align(text, width):

    fill_count = width - get_count_as_half_width(text)
    if (fill_count <= 0): return text

    return text + " "*fill_count
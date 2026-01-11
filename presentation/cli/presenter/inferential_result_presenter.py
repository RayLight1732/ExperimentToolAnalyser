from domain.analysis.inferential.result.inferential_result_history import (
    InferentialResultHistory,
)
from application.port.output.inferential_statistics_output_port import (
    InferentialResultOutputPort,
)
from domain.analysis.inferential.result.inferential_result import InferentialResult
from typing import List
from domain.value.subject import Subject


class InferentialResultPresenter(InferentialResultOutputPort):
    def present(
        self, subjects: List[Subject], result: InferentialResultHistory
    ) -> None:

        self._print_result(result.original)
        for post_process_result in result.post_process:
            self._print_result(post_process_result)

    def _print_result(self, result: InferentialResult):
        print(result.method)
        sorted_comparisons = sorted(
            result.comparisons.items(), key=lambda kv: str(kv[0])
        )
        for comparison in sorted_comparisons:
            left = comparison[0].left
            right = comparison[0].right
            if left != None and right != None:
                print(
                    left.mode,
                    right.mode,
                    comparison[1].p_value,
                )
            elif comparison[0].is_global:
                print("global", comparison[1].p_value)
            else:
                print("error:comparison is invalid")

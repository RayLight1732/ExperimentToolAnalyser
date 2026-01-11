from domain.analysis.inferential.result.inferential_result import InferentialResult
from domain.analysis.inferential.post_processor import PostProcessor
from statsmodels.stats.multitest import multipletests  # type: ignore[import-untyped]
from domain.analysis.inferential.result.evidence import Evidence
from typing import Dict
from domain.analysis.inferential.result.comparison import Comparison


class HolmPostProcessor(PostProcessor):

    def process(self, result: InferentialResult) -> InferentialResult:
        raw_items = list(result.comparisons.items())
        raw_p_values = [raw_item[1].p_value for raw_item in raw_items]
        _, corrected_pvalues, _, _ = multipletests(  # type: ignore
            raw_p_values, alpha=0.05, method="holm"
        )
        result_comparisons: Dict[Comparison, Evidence] = {}
        for i, corrected_p in enumerate(corrected_pvalues):
            result_comparisons[raw_items[i][0]] = Evidence(corrected_p)

        return InferentialResult("holm", result_comparisons)

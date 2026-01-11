from dataclasses import dataclass
from typing import List

from domain.analysis.inferential.result.inferential_result import InferentialResult


@dataclass(frozen=True)
class InferentialResultHistory:
    original: InferentialResult
    post_process: List[InferentialResult]

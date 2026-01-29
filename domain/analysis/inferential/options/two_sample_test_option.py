from domain.analysis.inferential.options.test_option import TestOption
from dataclasses import dataclass
from typing import List
from domain.analysis.inferential.result.comparison import Comparison

@dataclass
class TwoSampleTestOption(TestOption):
    comparisons:List[Comparison]
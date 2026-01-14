from application.dto.progress_phase import ProgressPhase
from application.dto.inferential_analysis_step import InferentialAnalysisStep


HOLM = ProgressPhase("holm", InferentialAnalysisStep.POST_PROCESS)
BONFERRONI = ProgressPhase("bonferroni", InferentialAnalysisStep.POST_PROCESS)

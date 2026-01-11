from application.model.progress_phase import ProgressPhase
from application.model.inferential_analysis_step import InferentialAnalysisStep


HOLM = ProgressPhase("holm", InferentialAnalysisStep.POST_PROCESS)
BONFERRONI = ProgressPhase("bonferroni", InferentialAnalysisStep.POST_PROCESS)

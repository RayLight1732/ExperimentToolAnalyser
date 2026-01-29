from application.port.output.progress_output_port import ProgressAdvanceOutputPort
from domain.analysis.inferential.inferential_calculator import InferentialCalculator
from domain.analysis.inferential.options.two_sample_test_option import TwoSampleTestOption
from infra.calculator.inferential.paired_t_test_calculator import PairedTTestCalculator
from infra.calculator.inferential.wilcoxon_calculator import WilcoxonCalculator


class CalculatorFactory:
    def create_wilcoxon_calculator(self,output_port:ProgressAdvanceOutputPort)->InferentialCalculator[TwoSampleTestOption]:
        return WilcoxonCalculator(output_port)
    
    def create_paired_t_test_calculator(self,output_Port:ProgressAdvanceOutputPort)->InferentialCalculator[TwoSampleTestOption]:
        return PairedTTestCalculator(output_Port)
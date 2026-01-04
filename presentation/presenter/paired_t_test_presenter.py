from application.dto.t_test_result_dto import CorrectedAndOriginalValueByConditionPair
from application.dto.value_type import ValueType
from application.port.output.calculator.run_paired_t_test_with_holm_output_port import (
    RunPairedTTestWithHolmOutputPort,
)


class PairedTTestPresenter(RunPairedTTestWithHolmOutputPort):
    def __init__(self, on_complete_callback=None):
        self.results = {}
        self.on_complete_callback = on_complete_callback

    def on_start(self, value_type: ValueType) -> None:
        pass

    def on_complete(
        self,
        value_type: ValueType,
        result: CorrectedAndOriginalValueByConditionPair,
    ) -> None:
        for condition_pair, t_test_result in result.values.items():
            print(
                f"Paired T-Test Result for {condition_pair[0].mode.display_name} vs {condition_pair[1].mode.display_name}:"
            )
            print(f"  Original p-value: {t_test_result.original}")
            print(f"  Corrected p-value: {t_test_result.corrected}")
            print("")
        if self.on_complete_callback is not None:
            self.on_complete_callback(value_type, result)

    def on_error(
        self,
        value_type: ValueType,
        error: Exception,
    ) -> None:
        pass

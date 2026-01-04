from application.port.output.collect_value_output_port import (
    CollectValueOutputPort,
)
from application.dto.value_type import ValueType
from domain.value_object.grouped_value import GroupedValue


class CollectValuePresenter(CollectValueOutputPort):
    def on_start(self, value_type: ValueType) -> None:
        print(f"Starting collection for {value_type.name}.")

    def on_progress(self, value_type: ValueType, current: int, total: int) -> None:
        print(f"Collecting {value_type.name}: {current}/{total} completed.")

    def on_error(self, value_type: ValueType, error: Exception) -> None:
        print(f"Error during collection of {value_type.name}: {str(error)}")

    def on_complete(self, value_type: ValueType, result: GroupedValue[float]) -> None:
        print(f"Completed collection for {value_type.name}.")
        if value_type == ValueType.AVERAGE_COP_SPEED:
            for condition, values in result.value.items():
                for subject, value in values.items():
                    print(condition, subject.name, value)

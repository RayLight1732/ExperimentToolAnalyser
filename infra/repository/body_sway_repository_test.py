from pytest_mock import MockerFixture
from infra.repository.body_sway_repository import BodySwayRepository
from domain.value.condition import Condition, CoolingMode, Position
from datetime import datetime
from domain.value.body_sway import BodySway, COP
from domain.value.subject_data import SubjectData
import pytest
from domain.repository.error.body_sway_format_error import BodySwayFormatError


def test_body_sway_repository(mocker: MockerFixture) -> None:
    path_resolver_mock = mocker.Mock()

    path_resolver_mock.body_sway_path.return_value = "some/path/to/body_sway.csv"

    file_system_mock = mocker.Mock()

    file_system_mock.load_csv.return_value = [
        ["Time", "X", "Y"],  # Header
        ["0.0", "0.0", "0.0"],
        ["0.1", "1.0", "1.0"],
        ["0.2", "2.0", "2.0"],
        ["", "", ""],  # Empty line at the end
    ]

    time = datetime(2024, 1, 1, 12, 0, 0)

    repo = BodySwayRepository(path_resolver_mock, file_system_mock)
    result = repo.load(
        SubjectData("subject1"), Condition(CoolingMode.ALWAYS, Position.CAROTID), time
    )

    expected = BodySway(
        cop_points=[
            COP(x=0.0, y=0.0, time=0.0),
            COP(x=1.0, y=1.0, time=0.1),
            COP(x=2.0, y=2.0, time=0.2),
        ]
    )

    path_resolver_mock.body_sway_path.assert_called_once_with(
        "subject1", Condition(CoolingMode.ALWAYS, Position.CAROTID), time
    )
    file_system_mock.load_csv.assert_called_once_with("some/path/to/body_sway.csv")
    assert result == expected


def test_body_sway_repository_error_on_middle_empty_line(
    mocker: MockerFixture,
) -> None:
    path_resolver_mock = mocker.Mock()
    path_resolver_mock.body_sway_path.return_value = "some/path/to/body_sway.csv"

    file_system_mock = mocker.Mock()
    file_system_mock.load_csv.return_value = [
        ["Time", "X", "Y"],  # Header
        ["0.0", "0.0", "0.0"],
        ["", "", ""],  # ← 途中の空白行（仕様違反）
        ["0.1", "1.0", "1.0"],
    ]

    time = datetime(2024, 1, 1, 12, 0, 0)

    repo = BodySwayRepository(path_resolver_mock, file_system_mock)

    with pytest.raises(BodySwayFormatError):
        repo.load(
            SubjectData("subject1"),
            Condition(CoolingMode.ALWAYS, Position.CAROTID),
            time,
        )

    path_resolver_mock.body_sway_path.assert_called_once_with(
        "subject1", Condition(CoolingMode.ALWAYS, Position.CAROTID), time
    )
    file_system_mock.load_csv.assert_called_once_with("some/path/to/body_sway.csv")

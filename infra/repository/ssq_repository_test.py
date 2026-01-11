import pytest
from datetime import datetime

from infra.repository.ssq_repository import SSQRepository
from domain.value.condition import Condition
from domain.value.time_point import TimePoint
from domain.repository.error.ssq_not_found_error import SSQNotFoundError
from domain.value.ssq_format_error import SSQFormatError
from domain.value.ssq import SSQ
from typing import List, Type
from dataclasses import dataclass


def test_get_ssq_returns_ssq(mocker):
    # --- arrange ---
    path_resolver = mocker.Mock()
    file_system = mocker.Mock()

    name = "test_user"
    condition = mocker.Mock(spec=Condition)
    time_point = mocker.Mock(spec=TimePoint)
    timestamp = datetime(2025, 1, 1, 12, 0, 0)

    path = "/dummy/path/ssq.csv"
    path_resolver.ssq_path.return_value = path

    csv_row = [
        "1",
        "2",
        "3",
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
    ]
    file_system.load_csv.return_value = iter([csv_row])

    repo = SSQRepository(
        path_resolver=path_resolver,
        file_system=file_system,
    )

    # --- act ---
    result = repo.get_ssq(name, condition, time_point, timestamp)

    # --- assert ---
    assert result == SSQ((1, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
    path_resolver.ssq_path.assert_called_once_with(
        name, condition, time_point, timestamp
    )
    file_system.load_csv.assert_called_once_with(path)


def test_get_ssq_raises_error_when_csv_empty(mocker):
    # --- arrange ---
    path_resolver = mocker.Mock()
    file_system = mocker.Mock()

    name = "test_user"
    condition = mocker.Mock(spec=Condition)
    time_point = mocker.Mock(spec=TimePoint)
    timestamp = datetime(2025, 1, 1, 12, 0, 0)

    path = "/dummy/path/ssq.csv"
    path_resolver.ssq_path.return_value = path

    file_system.load_csv.return_value = iter([])

    repo = SSQRepository(
        path_resolver=path_resolver,
        file_system=file_system,
    )

    # --- act & assert ---
    with pytest.raises(SSQNotFoundError) as exc:
        repo.get_ssq(name, condition, time_point, timestamp)

    assert exc.value.path == path


@dataclass(frozen=True)
class ErrorTestCase:
    name: str
    return_value: List[str]
    err: Type[Exception]


@pytest.mark.parametrize(
    "error_tc",
    [
        ErrorTestCase(
            name="invalid col count",
            return_value=["0", "1", "2"],
            err=SSQFormatError,
        ),
        ErrorTestCase(
            name="invalid value",
            return_value=[
                "a","0","0","0","0",
                "0","0","0","0","0",
                "0","0","0","0","0",
                "0",
            ],
            err=ValueError,
        ),
    ],
    ids=lambda tc: tc.name,
)
def test_get_ssq_raises_error(error_tc: ErrorTestCase, mocker):
    # --- arrange ---
    path_resolver = mocker.Mock()
    file_system = mocker.Mock()

    name = "test_user"
    condition = mocker.Mock(spec=Condition)
    time_point = mocker.Mock(spec=TimePoint)
    timestamp = datetime(2025, 1, 1, 12, 0, 0)

    path = "/dummy/path/ssq.csv"
    path_resolver.ssq_path.return_value = path

    file_system.load_csv.return_value = iter([error_tc.return_value])

    repo = SSQRepository(
        path_resolver=path_resolver,
        file_system=file_system,
    )

    # --- act & assert ---
    with pytest.raises(error_tc.err):
        repo.get_ssq(name, condition, time_point, timestamp)

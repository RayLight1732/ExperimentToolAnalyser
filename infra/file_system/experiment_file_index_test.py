import pytest
from datetime import datetime

from infra.dto.session_files import SessionFileCandidates, ExperimentFile
from infra.file_system.experiment_file_index import ExperimentFileIndex
from infra.dto.session_files import FileKind
from infra.file_system.file_name_parser import FileNameParser
from domain.value_object.condition import Condition, CoolingMode, Position
from pytest_mock import MockerFixture
from typing import Dict, List


@pytest.fixture
def parser(mocker: MockerFixture):
    mock = mocker.Mock()
    mock.parse.return_value = (FileKind.BODY_SWAY, datetime(2002, 1, 1))
    return mock


def test_list_subjects(parser: FileNameParser, mocker: MockerFixture) -> None:
    file_system_mock = mocker.Mock()
    tree: Dict[str, List[str]] = {
        "\\data": ["なし", "常時"],
        "\\data\\なし": ["なし"],
        "\\data\\なし\\なし": ["subject1"],
        "\\data\\なし\\なし\\subject1": [],
        "\\data\\常時": ["頸動脈", "首筋"],
        "\\data\\常時\\頸動脈": ["subject2"],
        "\\data\\常時\\頸動脈\\subject2": [],
        "\\data\\常時\\首筋": ["subject2"],
        "\\data\\常時\\首筋\\subject2": [],
    }
    file_system_mock.listdir.side_effect = lambda path: tree.get(path, [])  # type: ignore
    file_system_mock.isdir.side_effect = lambda path: path in tree  # type: ignore

    resolver = mocker.Mock()
    resolver.working_dir = "\\data"
    resolver.subject_path.return_value = ""

    index = ExperimentFileIndex(file_system_mock, resolver, parser)

    subjects = index.list_subjects()

    assert subjects == ["subject1", "subject2"]


def test_list_sessions(parser: FileNameParser, mocker: MockerFixture) -> None:
    tree: Dict[str, List[str]] = {
        "\\data": ["なし", "常時"],
        "\\data\\なし": ["なし"],
        "\\data\\なし\\なし": ["subject1"],
        "\\data\\なし\\なし/subject1": [],
        "\\data\\常時": ["頸動脈", "首筋"],
        "\\data\\常時\\頸動脈": ["subject2"],
        "\\data\\常時\\頸動脈\\subject2": [],
        "\\data\\常時\\首筋": ["subject2"],
        "\\data\\常時\\首筋\\subject2": [],
    }
    file_system_mock = mocker.Mock()
    file_system_mock.listdir.side_effect = lambda path: tree.get(path, [])  # type: ignore
    file_system_mock.isdir.side_effect = lambda path: path in tree  # type: ignore

    resolver = mocker.Mock()
    resolver.working_dir = "\\data"
    resolver.subject_path.return_value = ""
    index = ExperimentFileIndex(file_system_mock, resolver, parser)

    sessions = index.list_sessions("subject2")

    assert sessions == {
        Condition(CoolingMode.ALWAYS, Position.CAROTID),
        Condition(CoolingMode.ALWAYS, Position.NECK),
    }


def test_scan_with_mocked_parser(parser: FileNameParser, mocker: MockerFixture) -> None:
    # Arrange
    tree = {
        "\\data\\ALWAYS\\CAROTID\\subject1": [
            "file1.csv",
            "file2.csv",
            "ignore.txt",
        ]
    }

    file_system_mock = mocker.Mock()
    file_system_mock.listdir.side_effect = lambda path: tree.get(path, [])  # type: ignore
    file_system_mock.isdir.side_effect = lambda path: path in tree  # type: ignore

    resolver = mocker.Mock()
    resolver.working_dir = "\\data"
    resolver.subject_path.return_value = "\\data\\ALWAYS\\CAROTID\\subject1"

    parser = mocker.Mock()
    parser.parse.side_effect = [
        (FileKind.SSQ_BEFORE, datetime(2024, 1, 1, 12, 0, 0)),
        (FileKind.FMS, datetime(2024, 1, 1, 12, 10, 0)),
        None,
    ]

    index = ExperimentFileIndex(file_system_mock, resolver, parser)

    # Act
    result = index.scan(
        subject_name="subject1",
        condition=Condition(CoolingMode.ALWAYS, Position.CAROTID),
    )

    # Assert
    assert len(result.files) == 2
    assert SessionFileCandidates(
        [
            ExperimentFile(
                "\\data\\ALWAYS\\CAROTID\\subject1\\file1.csv",
                FileKind.SSQ_BEFORE,
                datetime(2024, 1, 1, 12, 0, 0),
            ),
            ExperimentFile(
                "\\data\\ALWAYS\\CAROTID\\subject1\\file2.csv",
                FileKind.FMS,
                datetime(2024, 1, 1, 12, 10, 0),
            ),
        ]
    )
    kinds = {f.kind for f in result.files}
    assert kinds == {FileKind.SSQ_BEFORE, FileKind.FMS}

    parser.parse.assert_any_call("file1.csv")
    parser.parse.assert_any_call("file2.csv")
    parser.parse.assert_any_call("ignore.txt")
    assert parser.parse.call_count == 3

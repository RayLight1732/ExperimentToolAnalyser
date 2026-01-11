from pytest_mock import MockerFixture
from infra.repository.session_repository import SessionRepository
from datetime import datetime, timedelta
from infra.dto.session_files import ExperimentFile, FileKind
from domain.value.subject import TrialResultSummary
from domain.value.time_point import TimePoint


def test_try_build_summary_with_valid_value(mocker: MockerFixture):
    index_mock = mocker.Mock()
    session_repo = SessionRepository(index_mock)

    ts = datetime(2025, 1, 1)
    questionnaire_files = [
        ExperimentFile("path1", FileKind.SSQ_BEFORE, ts),
        ExperimentFile("path2", FileKind.SSQ_AFTER, ts),
        ExperimentFile("path3", FileKind.FMS, ts),
    ]

    ts2 = ts + timedelta(minutes=3)
    body_sways = [ExperimentFile("path4", FileKind.BODY_SWAY, ts2)]
    result = session_repo._try_build_summary(ts, questionnaire_files, body_sways)

    assert result == TrialResultSummary(
        {TimePoint.BEFORE: ts, TimePoint.AFTER: ts}, ts, ts2
    )


def test_find_body_sway_with_valid_value(mocker: MockerFixture):
    index_mock = mocker.Mock()
    session_repo = SessionRepository(index_mock)

    result = session_repo._find_body_sway(
        datetime(2025, 1, 1, 0, 0, 0),
        [
            ExperimentFile("file1", FileKind.BODY_SWAY, datetime(2025, 1, 1, 0, 5, 0)),
            ExperimentFile("file2", FileKind.BODY_SWAY, datetime(2025, 1, 1, 0, 6, 0)),
            ExperimentFile("file3", FileKind.BODY_SWAY, datetime(2025, 1, 1, 0, 15, 0)),
        ],
    )

    assert result == ExperimentFile(
        "file1", FileKind.BODY_SWAY, datetime(2025, 1, 1, 0, 5, 0)
    )

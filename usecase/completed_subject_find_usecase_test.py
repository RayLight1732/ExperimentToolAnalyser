from typing import List
from unittest.mock import Mock

import pytest
from pytest_mock import MockerFixture

from usecase.completed_subject_find_usecase import CompletedSubjectFindUsecase
from domain.value_object.condition import CoolingMode, Position,Condition


@pytest.fixture
def usecase(mocker: MockerFixture) -> CompletedSubjectFindUsecase:
    mock_repo: Mock = mocker.Mock()
    return CompletedSubjectFindUsecase(mock_repo)


def test_is_valid_subject_true(
    usecase: CompletedSubjectFindUsecase,
    mocker: MockerFixture,
) -> None:
    sessions = [
        mocker.Mock(condition=Condition(CoolingMode.NONE)),
        mocker.Mock(condition=Condition(CoolingMode.ALWAYS, Position.CAROTID)),
        mocker.Mock(condition=Condition(CoolingMode.PERIODIC, Position.CAROTID)),
        mocker.Mock(condition=Condition(CoolingMode.SICK_SCENE_ONLY, Position.CAROTID)),
    ]

    subject = mocker.Mock(sessions=sessions)

    assert usecase._has_all_required_conditions(subject) is True


def test_is_valid_subject_invalid_position(
    usecase: CompletedSubjectFindUsecase,
    mocker: MockerFixture,
) -> None:
    sessions: List[Mock] = [
        mocker.Mock(condition=Condition(CoolingMode.NONE)),
        mocker.Mock(condition=Condition(CoolingMode.ALWAYS,Position.NECK)),
        mocker.Mock(condition=Condition(CoolingMode.PERIODIC, Position.CAROTID)),
        mocker.Mock(condition=Condition(CoolingMode.SICK_SCENE_ONLY, Position.CAROTID)),
    ]

    subject: Mock = mocker.Mock(sessions=sessions)

    assert usecase._has_all_required_conditions(subject) is False


def test_is_valid_subject_missing_condition(
    usecase: CompletedSubjectFindUsecase,
    mocker: MockerFixture,
) -> None:
    sessions: List[Mock] = [
        mocker.Mock(condition=Condition(CoolingMode.NONE)),
        mocker.Mock(condition=Condition(CoolingMode.ALWAYS,Position.CAROTID)),
    ]

    subject: Mock = mocker.Mock(sessions=sessions)

    assert usecase._has_all_required_conditions(subject) is False


def test_is_valid_subject_duplicate_condition(
    usecase: CompletedSubjectFindUsecase,
    mocker: MockerFixture,
) -> None:
    sessions: List[Mock] = [
        mocker.Mock(condition=Condition(CoolingMode.NONE)),
        mocker.Mock(condition=Condition(CoolingMode.NONE)),
        mocker.Mock(condition=Condition(CoolingMode.ALWAYS, Position.CAROTID)),
        mocker.Mock(condition=Condition(CoolingMode.PERIODIC, Position.CAROTID)),
        mocker.Mock(condition=Condition(CoolingMode.SICK_SCENE_ONLY, Position.CAROTID)),
    ]

    subject: Mock = mocker.Mock(sessions=sessions)

    assert usecase._has_all_required_conditions(subject) is False

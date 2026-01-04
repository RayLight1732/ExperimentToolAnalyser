from typing import List
from unittest.mock import Mock

import pytest
from pytest_mock import MockerFixture

from application.usecase.list_completed_subjects_usecase import (
    ListCompletedSubjectsUsecase,
)
from domain.value_object.condition import CoolingMode, Position, Condition


@pytest.fixture
def usecase(mocker: MockerFixture) -> ListCompletedSubjectsUsecase:
    mock_repo: Mock = mocker.Mock()
    return ListCompletedSubjectsUsecase(mock_repo)


def test_is_valid_subject_true(
    usecase: ListCompletedSubjectsUsecase,
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
    usecase: ListCompletedSubjectsUsecase,
    mocker: MockerFixture,
) -> None:
    sessions: List[Mock] = [
        mocker.Mock(condition=Condition(CoolingMode.NONE)),
        mocker.Mock(condition=Condition(CoolingMode.ALWAYS, Position.NECK)),
        mocker.Mock(condition=Condition(CoolingMode.PERIODIC, Position.CAROTID)),
        mocker.Mock(condition=Condition(CoolingMode.SICK_SCENE_ONLY, Position.CAROTID)),
    ]

    subject: Mock = mocker.Mock(sessions=sessions)

    assert usecase._has_all_required_conditions(subject) is False


def test_is_valid_subject_missing_condition(
    usecase: ListCompletedSubjectsUsecase,
    mocker: MockerFixture,
) -> None:
    sessions: List[Mock] = [
        mocker.Mock(condition=Condition(CoolingMode.NONE)),
        mocker.Mock(condition=Condition(CoolingMode.ALWAYS, Position.CAROTID)),
    ]

    subject: Mock = mocker.Mock(sessions=sessions)

    assert usecase._has_all_required_conditions(subject) is False


def test_is_valid_subject_duplicate_condition(
    usecase: ListCompletedSubjectsUsecase,
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

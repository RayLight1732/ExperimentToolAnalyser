from domain.repository.subject_repository import SubjectRepository
from domain.entity.subject import Subject
from typing import List, Set
from domain.value_object.condition import CoolingMode, Position, Condition
from application.port.input.list_completed_subjects_input_port import (
    ListCompletedSubjectInputPort,
)


class ListCompletedSubjectsUsecase(ListCompletedSubjectInputPort):

    REQUIRED_CONDITIONS: Set[Condition] = {
        Condition(CoolingMode.NONE, None),
        Condition(CoolingMode.ALWAYS, Position.CAROTID),
        Condition(CoolingMode.PERIODIC, Position.CAROTID),
        Condition(CoolingMode.SICK_SCENE_ONLY, Position.CAROTID),
    }

    def __init__(self, subject_repo: SubjectRepository):
        self.subject_repo = subject_repo

    def execute(self) -> List[Subject]:
        subjects = self.subject_repo.list_subjects()
        valid_subjects = [
            subject
            for subject in subjects
            if self._has_all_required_conditions(subject)
        ]

        return valid_subjects

    def _has_all_required_conditions(self, subject: Subject):
        condition_set: Set[Condition] = set()
        for session in subject.sessions:
            condition_set.add(session.condition)
        return (
            len(condition_set) == len(subject.sessions)
            and condition_set == self.REQUIRED_CONDITIONS
        )

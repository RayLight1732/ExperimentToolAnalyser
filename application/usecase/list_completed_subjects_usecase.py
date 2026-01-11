from domain.value.condition import Condition
from domain.repository.subject_repository import SubjectRepository
from domain.value.subject import Subject
from typing import List, Set


class ListCompletedSubjectsUsecase:

    def __init__(self, subject_repo: SubjectRepository):
        self.subject_repo = subject_repo

    def execute(self, required: Set[Condition]) -> List[Subject]:
        return [
            subject
            for subject in self.subject_repo.list_subjects()
            if subject.completed(required)
        ]

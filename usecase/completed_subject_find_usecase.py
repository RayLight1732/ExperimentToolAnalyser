from domain.repository.subject_repository import SubjectRepository
from domain.repository.session_repository import SessionRepository
from domain.entity.subject import Subject
from typing import List,Set,Optional,Tuple
from domain.value_object.condition import CoolingMode,Position,Condition
from abc import ABC,abstractmethod

class CompletedSubjectFindUsecaseInterface(ABC):
    @abstractmethod
    def execute(self)->List[Subject]:
        pass

class CompletedSubjectFindUsecase(CompletedSubjectFindUsecaseInterface):

    REQUIRED_CONDITIONS: Set[Condition] = {
        Condition(CoolingMode.NONE, None),
        Condition(CoolingMode.ALWAYS, Position.CAROTID),
        Condition(CoolingMode.PERIODIC, Position.CAROTID),
        Condition(CoolingMode.SICK_SCENE_ONLY, Position.CAROTID),
    }
    def __init__(self,subject_repo:SubjectRepository):
        self.subject_repo = subject_repo

    def execute(self)->List[Subject]:
        subjects = self.subject_repo.list_subjects()
        valid_subjects = [subject for subject in subjects if self._has_all_required_conditions(subject)]

        return valid_subjects


    def _has_all_required_conditions(self,subject:Subject):
        condition_set:Set[Condition] = set()
        for session in subject.sessions:
            condition_set.add(session.condition)
        return len(condition_set) == len(subject.sessions) and condition_set == self.REQUIRED_CONDITIONS
    
def new_completed_subject_find_usecase(subject_repo:SubjectRepository):
    return CompletedSubjectFindUsecase(subject_repo)
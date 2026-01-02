from domain.repository.subject_repository import SubjectRepository as ISubjectRepository
from domain.entity.subject import Subject,Session
from domain.repository.session_repository import SessionRepository
from domain.value_object.subject_data import SubjectData
from typing import Sequence,List
from infra.file_system.experiment_file_index import ExperimentFileIndex

class SubjectRepository(ISubjectRepository):
    def __init__(self,file_index:ExperimentFileIndex,session_repo:SessionRepository):
        self.file_index = file_index
        self.session_repo = session_repo

    def list_subjects(self)->Sequence[Subject]:
        subjects:List[Subject] = []
        for subject_name in self.file_index.list_subjects():
            sessions:List[Session] = []
            for condition in self.file_index.list_sessions(subject_name):        
                session = self.session_repo.get_session(subject_name,condition)
                sessions.append(session)
            subject = Subject(SubjectData(subject_name),sessions)
            subjects.append(subject)
        return subjects

def new_subject_repository(file_index:ExperimentFileIndex,session_repo:SessionRepository):
    return SubjectRepository(file_index,session_repo)
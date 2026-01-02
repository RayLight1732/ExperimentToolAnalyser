from domain.service.collector import Collector
from domain.entity.subject import Subject
from domain.value_object.subject_data import SubjectData
from usecase.grouped_value import GroupedValue
from domain.value_object.condition import Condition
from domain.repository.fms_repository import FMSRepository
from typing import List,Dict
from collections import defaultdict

class PeakFMSCollector(Collector[float]):
    def __init__(self,fms_repo:FMSRepository):
        super().__init__()
        self.fms_repo = fms_repo

    def collect(self, subjects: List[Subject]) -> GroupedValue[float]:
        result:Dict[Condition,Dict[SubjectData,float]] = defaultdict(lambda:dict())
        for subject in subjects:
            for session in subject.sessions:
                fms = self.fms_repo.get_fms(subject.data.name,session.condition,session.result.fms_timestamp)
                result[session.condition][subject.data] = fms.peak

        return GroupedValue(dict(result))

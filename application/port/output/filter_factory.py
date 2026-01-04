from abc import ABC, abstractmethod
from application.dto.filter_type import FilterType
from application.usecase.service.collector.filter.filter import Filter


class FilterFactory(ABC):
    @abstractmethod
    def get(self, filter_type: FilterType) -> Filter:
        pass

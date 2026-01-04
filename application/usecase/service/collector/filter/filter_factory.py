from application.port.output.filter_factory import FilterFactory
from application.dto.filter_type import FilterType
from application.usecase.service.collector.filter.filter import Filter


class FilterFactoryImpl(FilterFactory):

    def __init__(self, name_filter: Filter):
        self._collectors = {FilterType.NAME_FILTER: name_filter}

    def get(self, filter_type: FilterType) -> Filter:
        try:
            return self._collectors[filter_type]
        except KeyError:
            raise ValueError(f"Unsupported FilterType: {filter_type}")

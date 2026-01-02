import pytest

from infra.file_system.path_resolver import PathResolver
from domain.value_object.condition import CoolingMode,Position,Condition
from dataclasses import dataclass
@pytest.fixture
def resolver() -> PathResolver:
    return PathResolver("working_dir")

def test_resolver(resolver:PathResolver)->None:
    @dataclass
    class TestCase:
        subject_name:str
        condition:Condition
        expect:str

    test_cases = [
        TestCase("被験者",Condition(CoolingMode.NONE,None),"working_dir\\なし\\なし\\被験者"),
        TestCase("被験者",Condition(CoolingMode.ALWAYS,Position.CAROTID),"working_dir\\常時\\頸動脈\\被験者"),
        TestCase("被験者",Condition(CoolingMode.PERIODIC,Position.CAROTID),"working_dir\\周期的\\頸動脈\\被験者"),
        TestCase("被験者",Condition(CoolingMode.SICK_SCENE_ONLY,Position.NECK),"working_dir\\酔いやすい場面のみ\\首筋\\被験者"),
        ]
    
    for tc in test_cases:
        result = resolver.subject_path(tc.subject_name,tc.condition)
        assert result == tc.expect
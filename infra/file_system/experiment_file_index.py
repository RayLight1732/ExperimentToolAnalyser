from domain.value_object.condition import Condition,CoolingMode,Position
from typing import List,Tuple,Optional,Set
from infra.dto.session_files import SessionFileCandidates,ExperimentFile
from infra.file_system.path_resolver import PathResolver
from infra.file_system.file_name_parser import FileNameParser
from bootstrap.config import Config
from infra.file_system.file_system import FileSystem,OSFileSystem
import os

class ExperimentFileIndex:
    def __init__(self,file_system:FileSystem,path_resolver:PathResolver,parser:FileNameParser):
        self.fs = file_system
        self.path_resolver = path_resolver
        self.parser = parser

    def list_subjects(self) -> List[str]:
        subjects = set()

        for mode in self.fs.listdir(self.path_resolver.working_dir):
            mode_path = os.path.join(self.path_resolver.working_dir, mode)
            if not self.fs.isdir(mode_path):
                continue

            for sub in self.fs.listdir(mode_path):
                sub_path = os.path.join(mode_path, sub)
                if not self.fs.isdir(sub_path):
                    continue
                
                for subject in self.fs.listdir(sub_path):
                        subject_path = os.path.join(sub_path, subject)
                        if self.fs.isdir(subject_path):
                            subjects.add(subject)

        return sorted(subjects)

    def list_sessions(self, subject_name: str) -> Set[Condition]:
        sessions: set[Condition] = set()

        for mode in CoolingMode:
            mode_path = os.path.join(self.path_resolver.working_dir, mode.display_name)
            if not self.fs.isdir(mode_path):
                continue

            if mode.requires_position:
                for position in Position:
                    subject_path = os.path.join(
                        mode_path,
                        position.display_name,
                        subject_name,
                    )
                    if self.fs.isdir(subject_path):
                        sessions.add(Condition(mode, position))
            else:
                subject_path = os.path.join(
                    mode_path,
                    mode.display_name,
                    subject_name,
                )
                if self.fs.isdir(subject_path):
                    sessions.add(Condition(mode, None))

        return sessions

    def scan(
        self,
        subject_name: str,
        condition:Condition
    ) -> SessionFileCandidates:
        base = self.path_resolver.subject_path(subject_name, condition)
        candidates:List[ExperimentFile] = []
        for name in self.fs.listdir(base):
            if self.fs.isdir(os.path.join(base,name)):
                continue

            parsed = self.parser.parse(name)
            if parsed is None:
                continue

            ex_file = ExperimentFile(
                        path=os.path.join(base, name),
                        kind=parsed[0],
                        time_stamp=parsed[1]
                    )
            candidates.append(ex_file)

        return SessionFileCandidates(candidates)





def new_experiment_file_index(config:Config):
    fs = OSFileSystem()
    parser = FileNameParser()
    resolver = PathResolver(config.working_dir)
    return ExperimentFileIndex(fs,resolver,parser)
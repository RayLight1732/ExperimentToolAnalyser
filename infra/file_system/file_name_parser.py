from typing import Tuple,Optional
from infra.dto.session_files import FileKind
from datetime import datetime
import re

class FileNameParser:
    SSQ_PATTERN = re.compile(r"SSQ_(?P<date>\d{8})_(?P<time>\d{6})_(before|after)\.csv")
    FMS_PATTERN = re.compile(r"FMS_(?P<date>\d{8})_(?P<time>\d{6})\.csv")
    BODYSWAY_PATTERN = re.compile(r"(\d{12})\.csv")

    @staticmethod
    def parse_yyyymmddhhmmss(ts: str) -> datetime:
        return datetime.strptime(ts, "%Y%m%d%H%M%S")
    
    @staticmethod
    def parse_yymmddhhmmss(value: str) -> datetime:
        return datetime.strptime(value, "%y%m%d%H%M%S")

    def parse(self, filename: str) -> Optional[Tuple[FileKind,datetime]]:
        if m := self.SSQ_PATTERN.match(filename):
            if m.group(3) == "before":
                dt_str = m.group("date") + m.group("time")  # yyyymmddhhmmss
                return (FileKind.SSQ_BEFORE, self.parse_yyyymmddhhmmss(dt_str))
            elif m.group(3) == "after":
                dt_str = m.group("date") + m.group("time")  # yyyymmddhhmmss
                return (FileKind.SSQ_AFTER, self.parse_yyyymmddhhmmss(dt_str))
            else:
                return None
        if m := self.FMS_PATTERN.match(filename):
            dt_str = m.group("date") + m.group("time")  # yyyymmddhhmmss
            return (FileKind.FMS,self.parse_yyyymmddhhmmss(dt_str))

        if m := self.BODYSWAY_PATTERN.match(filename):
            return (FileKind.BODY_SWAY, self.parse_yymmddhhmmss(m.group(1)))

        return None
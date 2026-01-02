import pytest
from datetime import datetime

from infra.file_system.file_name_parser import FileNameParser
from infra.dto.session_files import FileKind


@pytest.fixture
def parser() -> FileNameParser:
    return FileNameParser()


def test_parse_ssq_before(parser: FileNameParser) -> None:
    filename = "SSQ_20240101_123045_before.csv"

    result = parser.parse(filename)
    assert result is not None
    kind, ts = result

    assert kind == FileKind.SSQ_BEFORE
    assert ts == datetime(2024, 1, 1, 12, 30, 45)


def test_parse_ssq_after(parser: FileNameParser) -> None:
    filename = "SSQ_20240101_123045_after.csv"

    result = parser.parse(filename)
    assert result is not None
    kind, ts = result

    assert kind == FileKind.SSQ_AFTER
    assert ts == datetime(2024, 1, 1, 12, 30, 45)


def test_parse_fms(parser: FileNameParser) -> None:
    filename = "FMS_20231231_235959.csv"

    result = parser.parse(filename)
    assert result is not None
    kind, ts = result

    assert kind == FileKind.FMS
    assert ts == datetime(2023, 12, 31, 23, 59, 59)


def test_parse_body_sway(parser: FileNameParser) -> None:
    filename = "250101123045.csv"  # yymmddhhmmss

    result = parser.parse(filename)
    assert result is not None
    kind, ts = result

    assert kind == FileKind.BODY_SWAY
    assert ts == datetime(2025, 1, 1, 12, 30, 45)


def test_parse_invalid_filename(parser: FileNameParser) -> None:
    filename = "invalid_file_name.csv"

    result = parser.parse(filename)

    assert result is None
